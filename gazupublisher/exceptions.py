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
