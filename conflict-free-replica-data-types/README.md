### Problem Statement
Study LWW-Element-Set and implement a state-based LWW-Element-Dictionary with test cases.
Similar to LWW-Element-Set, the dictionary variant you are going to implement will store a timestamp for each key-value pair. 
In addition to the lookup, add and remove operations, the dictionary variant will also allow updating the value of a key. 
There should be a function to merge two dictionaries. Test cases should be clearly written and document what aspect of CRDT they test
Link: https://github.com/GoodNotes/interviews/blob/master/software-engineering.md

### Approach
- [ ] Understand Conflict Free Replica Data Types (CRDT) ✅
- [ ] Implement Last Write Wins Dictionary ✅
- [ ] Support lookup, add, remove & update operations ✅
- [ ] Implement merge function to reach eventual consistent state ✅
- [ ] Think of multithreading scenarios, since merging will happen in background ✅
- [ ] Add unit tests ✅

### Installation
```bash
source venv/bin/activate # Activate python virtual env

pip install -r requirements.txt # Install dependencies
```

### References
https://www.youtube.com/watch?v=oyUHd894w18
https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type