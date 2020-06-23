"""
Module for Blender functions
"""

import bpy


def blender_print(data):
    """
    Print to display in the Blender console
    """
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == "CONSOLE":
                override = {"window": window, "screen": screen, "area": area}
                for line in str(data).split("\n"):
                    bpy.ops.console.scrollback_append(
                        override, text=str(line), type="OUTPUT"
                    )


def take_screenshot(output_path, extension):
    """
    Take a screenshot.
    Save the image at the given path with the given extension.
    """
    bpy.context.scene.render.image_settings.file_format = extension
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)
    blender_print("Generated screenshot at path " + output_path)


def list_cameras():
    """
    Return a list of tuple representing the Blender cameras.
    Each tuple contains a camera object and its name.
    """
    cameras = []
    for obj in bpy.data.objects:
        if obj.type == "CAMERA":
            cameras.append((obj.name, obj))
    return cameras


def set_camera(camera):
    """
    Set the rendering camera.
    """
    bpy.context.scene.camera = camera
