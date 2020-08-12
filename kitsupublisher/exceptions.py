class TranslationException(Exception):
    """
    Error raised when a translation file can't be found.
    """
    pass


class MediaNotSetUp(Exception):
    """
    Error raised when a media file can't be found or set up.
    """
    pass


class DataRetrievingError(Exception):
    """
    Error raised when some raw content has not been retrieved.
    """
    pass


class ContextNotFoundError(Exception):
    """
    Error raised when the context class of a software was not found.
    """
    pass


class InvalidNodeError(Exception):
    """
    Error raised when, in a nodal context (i.e. Houdini) a node is not found.
    """
    pass


class RenderCameraError(Exception):
    """
    Error raised when a render camera has failed to be set.
    """
    pass


class RenderNotSupported(Exception):
    """
    Error raised when a render is not currently supported.
    """
    pass


class OutputPathError(Exception):
    """
    Error raised when an output path is invalid.
    """
    pass
