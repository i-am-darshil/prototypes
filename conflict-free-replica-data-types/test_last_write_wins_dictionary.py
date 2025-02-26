from typing import Dict
import pytest

from last_write_wins_dictionary import LastWriteWinsDictionary, EventuallyConsistentDictValue


class TestEventuallyConsistentDict:

  @pytest.fixture()
  def eventually_consistent_dict(self):
    return LastWriteWinsDictionary()

  # Tests if insert operation inserts values in local state
  def test_put(self, eventually_consistent_dict):
    eventually_consistent_dict.put('key', 'value')
    assert eventually_consistent_dict.get('key') == 'value'

  # Tests if update operation overwrites values in local state
  def test_put_overwrite(self, eventually_consistent_dict):
    eventually_consistent_dict.put('key', 'value1')
    eventually_consistent_dict.put('key', 'value2')
    assert eventually_consistent_dict.get('key') == 'value2'

  # Tests if a delete operation removes values from local state
  def test_remove(self, eventually_consistent_dict):
    eventually_consistent_dict.put('key', 'value1')
    eventually_consistent_dict.remove('key')
    assert eventually_consistent_dict.get('key') is None

  # Tests different merge scenarios possible
  def test_merge(self, eventually_consistent_dict):
    # For keys with different timestamp values, the one with the latest timestamp should be chosen
    replicated_storage: Dict[any, EventuallyConsistentDictValue] = {}
    eventually_consistent_dict.put('key1', 'value1')
    replicated_storage['key2'] = EventuallyConsistentDictValue(value='value20', tombstone=False)
    eventually_consistent_dict.put('key2', 'value21')
    replicated_storage['key1'] = EventuallyConsistentDictValue(value=None, tombstone=True)

    # For keys with same timestamp values, the one with insert/update operation be preferred over delete operation
    eventually_consistent_dict.put('key3', 10)
    replicated_storage['key3'] = EventuallyConsistentDictValue(value=20, tombstone=True)
    eventually_consistent_dict._local_state['key3'].timestamp = replicated_storage['key3'].timestamp

    # For keys with same timestamp value and similar operation, prefer the value that is lexicographically larger
    eventually_consistent_dict.put('key4', 10)
    replicated_storage['key4'] = EventuallyConsistentDictValue(value=20, tombstone=False)
    eventually_consistent_dict._local_state['key4'].timestamp = replicated_storage['key4'].timestamp

    eventually_consistent_dict.put('key5', {'a': 5})
    replicated_storage['key5'] = EventuallyConsistentDictValue(value={'a': 6}, tombstone=False)
    eventually_consistent_dict._local_state['key5'].timestamp = replicated_storage['key4'].timestamp

    # Remove all tombstone keys after merge
    eventually_consistent_dict.remove("key6")

    eventually_consistent_dict.merge(replicated_storage)
    assert eventually_consistent_dict.get('key1') is None
    assert eventually_consistent_dict.get('key2') == 'value21'
    assert eventually_consistent_dict.get('key3') == 10
    assert eventually_consistent_dict.get('key4') == 20
    assert eventually_consistent_dict.get('key5') == {'a': 6}
    assert eventually_consistent_dict.get('key6') is None
