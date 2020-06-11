# -*- coding: utf-8 -*-
"""
Run the gazu viewer, a Qt app in Blender.
This code reuses this snippet : https://gitlab.com/snippets/1881226
Using a timed modal operator to keep the Qt GUI alive and communicate via
`queue.Queue`.
"""

import queue
import sys
import os

from Qt import QtCore, QtWidgets, QtGui

import bpy

gazupublisher_folder = ""


def custom_print(data):
    """
    Print to display in the Blender console.
    """
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == "CONSOLE":
                override = {"window": window, "screen": screen, "area": area}
                bpy.ops.console.scrollback_append(
                    override, text=str(data), type="OUTPUT"
                )


bl_info = {
    "name": "Qt Launcher",
    "author": "CGWire",
    "location": "Main Toolbar > Window > Launch Qt",
    "description": "Launch Qt",
    "category": "Launch Qt",
}


def _add_qt_timer(self):
    """Add a timer to the Qt app that triggers `_process_qt_queue`."""

    self._timer = QtCore.QTimer()
    self._timer.timeout.connect(self.process_queue)
    self._timer.start(1)


def _process_qt_queue(self):
    """
    Process queued functions.
    Look in `self._qt_queue` and process any functions in there.
    """
    while not self._qt_queue.empty():
        function = self._qt_queue.get()
        function()


class BlenderQtAppTimedQueue(bpy.types.Operator):
    """
    Run a Qt app inside of Blender, without blocking Blender.
    To avoid (threading?) issues, communication happens via `queue.Queue`.
    """

    bl_idname = "wm.launch_kitsu"
    bl_label = "Launch Kitsu"

    _app = None
    _window = None
    _timer = None
    _counter = 0
    _bpy_queue = queue.Queue()
    _qt_queue = queue.Queue()

    def invoke(self, context, event):
        try:
            self.add_gazu_publisher_location_to_sys_path()
        except:
            return {"CANCELLED"}

        import gazupublisher.working_context as w
        from gazupublisher.utils.connection import connect_user, configure_host
        from gazupublisher.__main__ import create_app, create_login_window

        custom_print("Launching Kitsu")

        configure_host("http://localhost/api")
        connect_user("admin@example.com", "mysecretpassword")
        w.working_context = "BLENDER"
        self._app = create_app()
        create_login_window(self._app)
        self._window = self._app.current_window
        self._window.setObjectName("login_window")
        self._window.logged_in.disconnect()
        self._window.logged_in.connect(
            lambda is_success: self.on_emit(is_success)
        )
        self.window_changed = False
        return self.execute(context)

    def on_emit(self, is_success):
        """
        The modal execution of the operator (Blender loop) and the signal
        emitted by the window (Qt event) were in conflict. The solution
        implemented here is to introduce a boolean indicating whether the login
        has been successful or not. Then the window is changed.
        """
        if is_success:
            self.window_changed = True

    def _execute_queued(self):
        """Execute queued functions."""
        while not self._bpy_queue.empty():
            function = self._bpy_queue.get()
            function()

    def modal(self, context, event):
        """Run modal."""
        if event.type == "TIMER":
            if self.window_changed:
                # When the login window has disappeared, change window
                if self._window.objectName() == "login_window":
                    from gazupublisher.__main__ import create_main_window

                    create_main_window(self._app)
                    self.change_window(context)
                    self.window_changed = False
                elif self._window.objectName() == "error_window":
                    self.change_window(context)
                    self.window_changed = False
                else:
                    self.cancel(context)
                    return {"FINISHED"}
            self._app.processEvents()
            self._execute_queued()

        return {"PASS_THROUGH"}

    def execute(self, context):
        """
        Process the event loop of the Qt app.
        """
        window_type = type(self._window)
        window_type.process_queue = _process_qt_queue
        window_type.add_timer = _add_qt_timer
        window_type._bpy_queue = self._bpy_queue
        window_type._qt_queue = self._qt_queue

        self._window.add_timer()
        self._window.show()

        wm = context.window_manager
        # Run every 0.001 seconds
        self._timer = wm.event_timer_add(0.001, window=context.window)
        wm.modal_handler_add(self)

        return {"RUNNING_MODAL"}

    def change_window(self, context):
        """ Update the window """
        self._window = self._app.current_window
        self.execute(context)

    def cancel(self, context):
        """Remove event timer when stopping the operator."""
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        self._window.deleteLater()
        self._app.quit()
        self._window = None
        self._app = None

    def add_gazu_publisher_location_to_sys_path(self):
        if not gazupublisher_folder:
            message = "The location of the gazu publisher module is not set. Please set it and restart Blender"
            custom_print(message)
            self.report({"ERROR"}, message)
            raise ImportError

        path_gazupublisher = os.path.normpath(gazupublisher_folder)
        if path_gazupublisher not in sys.path:
            sys.path.append(path_gazupublisher)

        try:
            import gazupublisher
        except:
            message = (
                "The gazu publisher module (expected at emplacement "
                + str(path_gazupublisher)
                + ") was not found."
            )
            custom_print(message)
            self.report({"ERROR"}, message)
            raise


def register():
    """
    Register the class and add the drawer to the menu
    """
    bpy.utils.register_class(BlenderQtAppTimedQueue)
    bpy.types.INFO_MT_window.append(menu_draw)


def unregister():
    """
    Unregister the class and delete the drawer from the menu
    """
    bpy.utils.unregister_class(BlenderQtAppTimedQueue)
    bpy.types.INFO_MT_window.remove(menu_draw)


def run_timed_modal_operator_queue():
    """Run the app with help of a timed modal operator."""
    register()


def menu_draw(self, context):
    self.layout.separator()
    self.layout.operator(BlenderQtAppTimedQueue.bl_idname)


if __name__ == "__main__":
    run_timed_modal_operator_queue()
