"""
Module that implements the software interface for Blender mode.
"""
import bpy

from gazupublisher.utils.dcc.software import SoftwareContext


class BlenderContext(SoftwareContext):
    def blender_print(self, data):
        """
        Print to display in the Blender console.
        """
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == "CONSOLE":
                    override = {
                        "window": window,
                        "screen": screen,
                        "area": area,
                    }
                    for line in str(data).split("\n"):
                        bpy.ops.console.scrollback_append(
                            override, text=str(line), type="OUTPUT"
                        )

    def setup_preview(self, output_path, extension):
        """
        Setup preview context.
        :param output_path: Output path for the preview
        :param extension: Format setting for Blender
        """
        bpy.context.scene.render.image_settings.file_format = extension
        bpy.context.scene.render.filepath = output_path

    def setup_preview_animation(self, output_path, extension, container):
        """
        Setup preview context for animations.
        The codec is set at H.264.
        :param output_path: Output path for the preview
        :param extension: Format setting for Blender
        :param container: Container.
        :return:
        """
        self.setup_preview(output_path, extension)
        bpy.context.scene.render.ffmpeg.codec = "H264"
        bpy.context.scene.render.ffmpeg.format = container

    def take_render_screenshot(
        self, output_path, extension, use_viewtransform=True
    ):
        """
        Take a screenshot using Cycles.
        Save the image at the given path with the given extension.
        """
        self.setup_preview(output_path, extension)
        bpy.ops.render.render(write_still=True)
        self.blender_print("Generated screenshot at path " + output_path)

    def take_viewport_screenshot(self, output_path, extension):
        """
        Take a screenshot using OpenGL.
        Save the image at the given path with the given extension.
        """
        self.setup_preview(output_path, extension)
        bpy.ops.render.opengl(write_still=True)
        self.blender_print("Generated screenshot at path " + output_path)

    def take_render_animation(
        self, output_path, container, use_viewtransform=True
    ):
        """
        Take an animation using Cycles.
        Save the video at the given path with the given extension (container).
        """
        self.setup_preview_animation(output_path, "FFMPEG", container)
        bpy.ops.render.render(animation=True, write_still=True)
        self.blender_print("Generated animation at path " + output_path)

    def take_viewport_animation(self, output_path, container):
        """
        Take an animation using OpenGL.
        Save the video at the given path with the given extension (container).
        """
        self.setup_preview_animation(output_path, "FFMPEG", container)
        bpy.ops.render.opengl(animation=True, write_still=True)
        self.blender_print("Generated animation at path " + output_path)

    def list_cameras(self):
        """
        Return a list of tuple representing the Blender cameras.
        Each tuple contains a camera object and its name.
        """
        cameras = []
        for obj in bpy.data.objects:
            if obj.type == "CAMERA":
                cameras.append((obj.name, obj))
        return cameras

    def set_camera(self, camera):
        """
        Set the rendering camera.
        Check first if the camera is well-defined.
        """
        assert camera is not None
        list_camera_object = [
            camera_obj for _, camera_obj in self.list_cameras()
        ]
        assert camera in list_camera_object
        bpy.context.scene.camera = camera

    def get_current_scene(self):
        return bpy.context.scene

    def get_current_color_space(self):
        scene = self.get_current_scene()
        return scene.sequencer_colorspace_settings.name

    def set_current_color_space(self, color_space):
        scene = self.get_current_scene()
        scene.sequencer_colorspace_settings.name = color_space

    def list_extensions(self, is_video):
        """
        Return a list of available extensions along with the ID of their compression
        algorithm in Blender.
        """
        return (
            [(".mp4", "MPEG4"), (".mov", "QUICKTIME")]
            if is_video
            else [(".png", "PNG"), (".jpg", "JPEG")]
        )
