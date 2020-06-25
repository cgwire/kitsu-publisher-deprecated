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


def setup_preview(output_path, extension):
    """
    Setup preview context
    :param output_path: Output path for the preview
    :param extension: Format setting for Blender
    """
    bpy.context.scene.render.image_settings.file_format = extension
    bpy.context.scene.render.filepath = output_path


def take_render_screenshot(output_path, extension):
    """
    Take a screenshot using Cycles.
    Save the image at the given path with the given extension.
    """
    setup_preview(output_path, extension)
    bpy.ops.render.render(write_still=True)
    blender_print("Generated screenshot at path " + output_path)


def take_viewport_screenshot(output_path, extension):
    """
    Take a screenshot using OpenGL.
    Save the image at the given path with the given extension.
    """
    bpy.context.scene.render.image_settings.file_format = extension
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.opengl(write_still=True)
    blender_print("Generated screenshot at path " + output_path)


def take_render_animation(extension, output_path):
    bpy.context.scene.render.image_settings.file_format = extension
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.render(animation=True, write_still=True)
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
    Check first if the camera is well-defined.
    """
    assert camera is not None
    list_camera_object = [camera_obj for _, camera_obj in list_cameras()]
    assert camera in list_camera_object
    bpy.context.scene.camera = camera

def get_current_scene():
    return bpy.context.scene

def get_current_color_space():
    scene = get_current_scene()
    return scene.sequencer_colorspace_settings.name

def set_current_color_space(color_space):
    scene = get_current_scene()
    scene.sequencer_colorspace_settings.name = color_space
