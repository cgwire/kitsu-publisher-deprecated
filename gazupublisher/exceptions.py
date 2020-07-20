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
