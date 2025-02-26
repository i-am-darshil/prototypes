from datetime import datetime, timezone
from typing import Dict

from read_write_lock import RWLock


class EventuallyConsistentDictValue:
  def __init__(self, value, tombstone) -> None:
    self.value = value
    self.timestamp = datetime.now(timezone.utc)
    self.tombstone = tombstone

# Thread safe implementation of Last Write Wins Dictionary
# This dictionary supports eventual consistency and resolves conflicts using Last Write Wins (LWW) strategy
class LastWriteWinsDictionary:
  def __init__(self) -> None:
    self._local_state: Dict[any, EventuallyConsistentDictValue] = {}
    self._local_lock = RWLock()

  def get(self, key: any) -> any:
    self._local_lock.acquire_read_lock()
    val: EventuallyConsistentDictValue = self._local_state.get(key, None)
    self._local_lock.release_read_lock()

    if val and not val.tombstone:
      return val.value

    return None

  def put(self, key: any, value: any) -> None:
    self._local_lock.acquire_write_lock()

    val = EventuallyConsistentDictValue(value, False)
    self._local_state[key] = val

    self._local_lock.release_write_lock()

  def remove(self, key: any) -> None:
    self._local_lock.acquire_write_lock()

    val: EventuallyConsistentDictValue = EventuallyConsistentDictValue(None, True)
    self._local_state[key] = val

    self._local_lock.release_write_lock()

  def merge(self, replicated_state: Dict[any, EventuallyConsistentDictValue]) -> None:
    self._local_lock.acquire_write_lock()

    for local_key, local_value in self._local_state.items():
      if local_key in replicated_state:
        replicated_value: EventuallyConsistentDictValue = replicated_state[local_key]

        # Choose the value with the latest timestamp (LWW)
        # In case of same timestamp values, prefer inserts/updates over deletes
        # In case of same timestamp values and same operation, prefer the value that is lexicographically larger
        # This makes the state consistent across all replicas
        self._local_state[local_key] = max(local_value, replicated_value,
                                           key=lambda v: (v.timestamp, not v.tombstone, str(v.value)))
        del replicated_state[local_key]

    for replicated_key, replicated_value in replicated_state.items():
      self._local_state[replicated_key] = replicated_value

    # Remove all tombstone keys from local state to avoid filling up the memory
    keys_to_delete = [k for k, v in self._local_state.items() if v.tombstone]

    for k in keys_to_delete:
      del self._local_state[k]

    self._local_lock.release_write_lock()
