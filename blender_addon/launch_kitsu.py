# -*- coding: utf-8 -*-
"""
Test for running a Qt app in Blender.
This code reuses this snippet : https://gitlab.com/snippets/1881226
Using a timed modal operator to keep the Qt GUI alive and communicate via
`queue.Queue`. So far this seems to work fine on Linux and Windows (macOS
is untested at the moment).

isort:skip_file
"""

pyqt5_path = "<your_pyqt5_path_here>"

import functools
import queue
import sys
import bpy

from pprint import pformat

sys.path.append(pyqt5_path)
from PyQt5 import QtCore, QtWidgets
from gazu_publisher.gazupublisher.__main__ import create_display_entities


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
    """Process queued functions.

    Look in `self._qt_queue` and process any functions in there.
    """

    while not self._qt_queue.empty():
        function = self._qt_queue.get()
        custom_print(
            f"Running `{function.func.__name__}` from the Qt queue..."
        )
        function()


def custom_print(data):
    # """
    # Override print to display to console
    # :param data: Any printable data
    # """
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == "CONSOLE":
                override = {"window": window, "screen": screen, "area": area}
                bpy.ops.console.scrollback_append(
                    override, text=str(data), type="OUTPUT"
                )


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
        custom_print("Init BlenderQtAppTimedQueue")
        self._app, self._window = create_display_entities()

    def _execute_queued(self):
        """Execute queued functions."""
        while not self._bpy_queue.empty():
            function = self._bpy_queue.get()
            custom_print(
                f"Running `{function.func.__name__}` from the Blender queue..."
            )
            function()

    def modal(self, context, event):
        """Run modal."""
        if event.type == "TIMER":
            if self._window and not self._window.isVisible():
                self.cancel(context)
                return {"FINISHED"}
            self._app.processEvents()
            self._execute_queued()
        return {"PASS_THROUGH"}

    def execute(self, context):
        """Process the event loop of the Qt app."""
        login_window_type = type(self._window)
        login_window_type.process_queue = _process_qt_queue
        login_window_type.add_timer = _add_qt_timer
        login_window_type._use_queue = True
        login_window_type._bpy_queue = self._bpy_queue
        login_window_type._qt_queue = self._qt_queue

        self._window.add_timer()
        self._window.show()

        wm = context.window_manager
        # Run every 0.001 seconds
        self._timer = wm.event_timer_add(0.001, window=context.window)
        wm.modal_handler_add(self)

        return {"RUNNING_MODAL"}

    def cancel(self, context):
        """Remove event timer when stopping the operator."""
        wm = context.window_manager
        wm.event_timer_remove(self._timer)


def register():
    bpy.utils.register_class(BlenderQtAppTimedQueue)
    bpy.types.INFO_MT_window.append(menu_draw)


def unregister():
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
