"""
Module that implements the software interface for standalone mode.
"""

from gazupublisher.utils.dcc.software import SoftwareContext


class StandaloneContext(SoftwareContext):

    def list_cameras(self):
        """
        Return a list of tuple representing fake cameras.
        """
        return [
            ("CameraStandAlone1", "CameraObject1"),
            ("CameraStandAlone2", "CameraObject2"),
        ]

    def list_extensions(self, is_video):
        """
        Return a list of tuple representing fake extensions.
        """
        return [(".ext1", ""), (".ext2", "")]

    def software_print(self, data):
        print(data)
