import threading
import time

import pytest

from read_write_lock import RWLock


class TestRWLock:
    @pytest.fixture(scope="class")
    def rw_lock(self):
        return RWLock()

    def test_multiple_readers_reading(self, rw_lock):
        event_obj = threading.Event()

        def reading():
            event_obj.wait()
            rw_lock.acquire_read_lock()
            time.sleep(0.1)
            assert rw_lock._readers >= 1
            rw_lock.release_read_lock()

        readers = [threading.Thread(target=reading) for i in range(10)]
        for r in readers:
            r.start()
        event_obj.set()
        for r in readers:
            r.join()

    def test_single_writer_writing_exclusively(self, rw_lock):
        event_obj = threading.Event()

        def writing():
            event_obj.wait()
            rw_lock.acquire_write_lock()
            time.sleep(0.1)
            assert rw_lock._writers == 1
            assert rw_lock._readers == 0
            rw_lock.release_write_lock()

        def reading():
            event_obj.wait()
            rw_lock.acquire_read_lock()
            time.sleep(0.1)
            assert rw_lock._writers == 0
            assert rw_lock._readers >= 1
            rw_lock.release_read_lock()

        readers = [threading.Thread(target=reading) for i in range(10)]
        writers = [threading.Thread(target=writing) for i in range(5)]

        for r in readers:
            r.start()
        for w in writers:
            w.start()

        event_obj.set()

        for r in readers:
            r.join()
        for w in writers:
            w.join()

