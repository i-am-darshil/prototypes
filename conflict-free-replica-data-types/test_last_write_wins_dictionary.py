from threading import Thread
from typing import Dict
import pytest

from last_write_wins_dictionary import LastWriteWinsDictionary, EventuallyConsistentDictValue


class TestEventuallyConsistentDict:

  @pytest.fixture()
  def eventually_consistent_dict(self):
    return LastWriteWinsDictionary()

  def test_put(self, eventually_consistent_dict):
    eventually_consistent_dict.put('key', 'value')
    assert eventually_consistent_dict.get('key') == 'value'

  def test_put_overwrite(self, eventually_consistent_dict):
    eventually_consistent_dict.put('key', 'value1')
    eventually_consistent_dict.put('key', 'value2')
    assert eventually_consistent_dict.get('key') == 'value2'

  def test_remove(self, eventually_consistent_dict):
    eventually_consistent_dict.put('key', 'value1')
    eventually_consistent_dict.remove('key')
    assert eventually_consistent_dict.get('key') is None

  def test_merge(self, eventually_consistent_dict):
    replicated_storage: Dict[any, EventuallyConsistentDictValue] = {}
    eventually_consistent_dict.put('key1', 'value1')
    replicated_storage['key2'] = EventuallyConsistentDictValue(value='value20', tombstone=False)
    eventually_consistent_dict.put('key2', 'value21')
    replicated_storage['key1'] = EventuallyConsistentDictValue(value=None, tombstone=True)

    eventually_consistent_dict.merge(replicated_storage)
    assert eventually_consistent_dict.get('key1') is None
    assert eventually_consistent_dict.get('key2') == 'value21'
