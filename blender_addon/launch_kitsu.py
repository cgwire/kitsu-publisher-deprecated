# -*- coding: utf-8 -*-
"""
Test for running a Qt app in Blender.
This code reuses this snippet : https://gitlab.com/snippets/1881226
Using a timed modal operator to keep the Qt GUI alive and communicate via
`queue.Queue`.

isort:skip_file
"""
import queue
from print.custom_print import print as custom_print
from Qt import QtCore, QtWidgets, QtGui
from gazupublisher.gazupublisher.__main__ import (
    create_app,
    create_login_window,
    create_main_window,
)
import gazupublisher.gazupublisher.working_context as context

import bpy
import subprocess

bl_info = {
    "name": "Qt Launcher",
    "author": "LedruRollin",
    "location": "Main Toolbar > Window > Launch Qt",
    "description": "Launch Qt",
    "category": "Launch Qt",
}


def install_dependencies():
    """
    Install all the dependencies.
    Blender manages its own packages : we have to download pip via ensurepip
    and then retrieve all the necessary modules.
    """
    py_exec = bpy.app.binary_path_python
    # Ensure pip is installed & update (pip is installed by default with 2.81)
    if bpy.app.version < (2, 81, 0):
        subprocess.call([str(py_exec), "-m", "ensurepip"])
        subprocess.call(
            [str(py_exec), "-m", "pip", "install", "--upgrade", "pip"]
        )

    # Install the Qt binding
    desired_binding = "PyQt5"
    if desired_binding == "PyQt5":
        subprocess.call(
            [str(py_exec), "-m", "pip", "install", "--user", "PyQt5"]
        )
    elif desired_binding == "PySide2":
        subprocess.call(
            [str(py_exec), "-m", "pip", "install", "--user", "PySide2"]
        )
    else:
        raise AssertionError(
            "The binding " + desired_binding + "isn't available"
        )

    # Install gazu and qtazu
    subprocess.call(
        [
            str(py_exec),
            "-m",
            "pip",
            "install",
            "--user",
            "git+https://github.com/LedruRollin/gazu.git",
        ]
    )
    subprocess.call([str(py_exec), "-m", "pip", "install", "--user", "qtazu"])


def uninstall_dependencies():
    py_exec = bpy.app.binary_path_python

    # Uninstall gazu and qtazu
    subprocess.call([str(py_exec), "-m", "pip", "uninstall", "-y", "gazu"])
    subprocess.call([str(py_exec), "-m", "pip", "uninstall", "-y", "qtazu"])


def _add_qt_timer(self):
    """Add a timer to the Qt app that triggers `_process_qt_queue`."""

    self._timer = QtCore.QTimer()
    self._timer.timeout.connect(self.process_queue)
    self._timer.start(1)


def _process_qt_queue(self):
    """Process queued functions.

    Look in `self._qt_queue` and process any functions in there.
    """

    while not self._qt_queue.empty():
        function = self._qt_queue.get()
        function()


class BlenderQtAppTimedQueue(bpy.types.Operator):
    """Run a Qt app inside of Blender, without blocking Blender.

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

    def __init__(self):

        custom_print("Launching Kitsu")

        from gazupublisher.gazupublisher.utils.connection import (
            connect_user,
            configure_host,
        )

        configure_host("http://localhost/api")
        # connect_user("admin@example.com", "mysecretpassword")
        global context
        context = "BLENDER"
        custom_print("Working context : " + context)

        self._app = create_app()
        create_login_window(self._app)
        self._window = self._app.current_window
        self._window.setObjectName("login_window")
        self._window.logged_in.disconnect()
        self._window.logged_in.connect(
            lambda is_success: self.on_emit(is_success)
        )
        self.login_success = False

    def on_emit(self, is_success):
        """
        The modal execution of the operator (Blender loop) and the signal
        emitted by the window (Qt event) were in conflict. The solution
        implemented here is to introduce a boolean indicating whether the login
        has been successful or not. Then the window is changed.
        """
        if is_success:
            self.login_success = True

    def _execute_queued(self):
        """Execute queued functions."""
        while not self._bpy_queue.empty():
            function = self._bpy_queue.get()
            function()

    def modal(self, context, event):
        """Run modal."""
        if event.type == "TIMER":
            if self.login_success:
                # When the login window has disappeared, change window
                if self._window.objectName() == "login_window":
                    self.change_window(context)
                    self.login_success = False
                else:
                    self.cancel(context)
                    return {"FINISHED"}
            self._app.processEvents()
            self._execute_queued()
        return {"PASS_THROUGH"}

    def execute(self, context):
        """Process the event loop of the Qt app."""
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
        create_main_window(self._app)
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
