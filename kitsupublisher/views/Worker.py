from Qt import QtCore


class Worker(QtCore.QRunnable):
    """
    Worker thread
    :param callback: The function callback to run on this worker thread.
                     Supplied args and kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """

    def __init__(self, function, *args, **kwargs):
        super(Worker, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    @QtCore.Slot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        self.function(*self.args, **self.kwargs)


class GazuWorker(QtCore.QRunnable):
    """
    Worker thread
    :param callback: The function callback to run on this worker thread.
                     Supplied args and kwargs will be passed through to the runner.
                     This function should have an interaction with the gazu API.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    This class is pretty similar to the already existing Worker class, one could
    see if unifying these two is possible.

    """

    def __init__(self, function, *args, **kwargs):
        super(GazuWorker, self).__init__()

        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.signals = GazuWorkerSignals()

    @QtCore.Slot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        self.signals.begun.emit()
        res = self.function(*self.args, **self.kwargs)
        self.signals.result.emit(res)
        self.signals.finished.emit()


class GazuWorkerSignals(QtCore.QObject):
    """
    Defines the signals available from a running worker thread.
    """

    begun = QtCore.Signal()
    finished = QtCore.Signal()
    result = QtCore.Signal(object)
