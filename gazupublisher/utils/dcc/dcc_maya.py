"""
Module for Maya functions
"""

import subprocess
import maya.cmds as cmds

from gazupublisher.utils.dcc.software import SoftwareContext


class MayaContext(SoftwareContext):
    def set_camera(self, camera):
        self.camera = camera

    def list_cameras(self):
        """
        Return a list of tuple representing the Maya cameras.
        Each tuple contains a camera name and its shape name.
        """
        res = []
        camera_names = cmds.listCameras()
        for camera_name in camera_names:
            camera_shape = cmds.listRelatives(
                camera_name, type="camera", s=True
            )[0]
            res.append((camera_name, camera_shape))
        return res

    def set_camera(self, camera_shape):
        """
        Set the rendering camera.
        Check first if the camera is well-defined.
        Then set the camera as renderable, and all the others as non renderable
        """
        all_camera_shapes = cmds.ls(type="camera")
        assert camera_shape in all_camera_shapes
        for shape in all_camera_shapes:
            cmds.setAttr(shape + ".renderable", shape == camera_shape)

    def take_viewport_screenshot(self, output_path, extension):
        """
        Take a screenshot of the current view.
        """
        file_extension, _ = extension
        cmds.refresh(cv=True, fe=file_extension, fn=output_path)

    def take_render_screenshot(
        self, output_path, extension, use_view_transform=True
    ):
        """
        Take a render using the command line.
        """
        pass

    def take_viewport_animation(self, output_path, extension):
        """
        Take a playblast of the current view.
        """
        cmds.playblast(
            filename=output_path,
            forceOverwrite=True,
            quality=100,
            percent=100,
            viewer=False,
            format="qt",
        )

    def take_render_animation(
        self, output_path, extension, use_view_transform=True
    ):
        """
        Take a render using the command line.
        """
        pass

    def list_extensions(self, is_video):
        """
        Return a list of available extensions along with the IDs of their compression
        algorithm in Maya.
        """
        return (
            [(".mov", "22")]
            if is_video
            else [(".png", ("png", "32")), (".jpg", ("jpg", "8"))]
        )
