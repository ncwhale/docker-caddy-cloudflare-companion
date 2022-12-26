import threading

class RepeatedRun(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._thread = None
        self.exit_event = threading.Event()
        self.exit_event.set() # Thread is not running when inited.

        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def _run(self):
        while not self.exit_event.is_set():
            self.function(*self.args, **self.kwargs)
            self.exit_event.wait(self.interval) # wait for flag set.

    def start(self):
        if self.exit_event.is_set():
            self.exit_event.clear()
            self._thread = threading.Thread(target=self._run, name=str(self.function))
            self._thread.start()

    def stop(self):
        self.exit_event.set() # This will set flag and let the running thread weakup.

        if self._thread is not None:
            self._thread.join() # Wait for thread done their job.
            self._thread = None
