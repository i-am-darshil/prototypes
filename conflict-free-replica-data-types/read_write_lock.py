from threading import Condition


class RWLock:
    def __init__(self):
        self._condition = Condition()
        self._readers = 0
        self._writers = 0
        self._waiting_writers = 0

    def acquire_read_lock(self):
        with self._condition:
            while self._writers > 0 or self._waiting_writers > 0:
                self._condition.wait()
            self._readers += 1

    def release_read_lock(self):
        with self._condition:
            self._readers -= 1 if self._readers > 0 else 0
            if self._readers == 0:
                self._condition.notify_all()

    def acquire_write_lock(self):
        with self._condition:
            self._waiting_writers += 1
            while self._readers > 0 or self._writers > 0:
                self._condition.wait()
            self._waiting_writers -= 1
            self._writers += 1

    def release_write_lock(self):
        with self._condition:
            self._writers -= 1
            self._condition.notify_all()