from datetime import datetime, timezone
from typing import Dict

from read_write_lock import RWLock


class EventuallyConsistentDictValue:
  def __init__(self, value, tombstone) -> None:
    self.value = value
    self.timestamp = datetime.now(timezone.utc)
    self.tombstone = tombstone

class LastWriteWinsDictionary:
  def __init__(self) -> None:
    self.local_state: Dict[any, EventuallyConsistentDictValue] = {}
    self.local_lock = RWLock()

  def put(self, key: any, value: any) -> None:
    self.local_lock.acquire_write_lock()

    val = EventuallyConsistentDictValue(value, False)
    self.local_state[key] = val

    self.local_lock.release_write_lock()

  def remove(self, key: any) -> None:
    self.local_lock.acquire_write_lock()

    val: EventuallyConsistentDictValue = EventuallyConsistentDictValue(None, True)
    self.local_state[key] = val

    self.local_lock.release_write_lock()

  def merge(self, replicated_state: Dict[any, EventuallyConsistentDictValue]) -> None:
    self.local_lock.acquire_write_lock()

    for local_key, local_value in self.local_state.items():
      if local_key in replicated_state:
        replicated_value: EventuallyConsistentDictValue = replicated_state[local_key]
        # Choose the value with the latest timestamp (LWW)
        self.local_state[local_key] = max(local_value, replicated_value, key=lambda v: v.timestamp)
        del replicated_state[local_key]

    for replicated_key, replicated_value in replicated_state.items():
      self.local_state[replicated_key] = replicated_value

    keys_to_delete = [k for k, v in self.local_state.items() if v.tombstone]

    for k in keys_to_delete:
      del self.local_state[k]

    self.local_lock.release_write_lock()

  def get(self, key: any) -> any:
    self.local_lock.acquire_read_lock()
    val: EventuallyConsistentDictValue = self.local_state.get(key, None)
    self.local_lock.release_read_lock()

    if val and not val.tombstone:
      return val.value

    return None
