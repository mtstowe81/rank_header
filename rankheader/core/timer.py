import time

class Timer:
    '''
    Timer for python operations.

    Attributes
    ----------
    start: float
        The start time in seconds of the operation.
    end: float
        The end time in seconds of the operation.
    interval: float
        The elapsed time in seconds of the operation.
    '''
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.interval = self.end - self.start