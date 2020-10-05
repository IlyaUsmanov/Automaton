# automaton

Converts your automaton to minimal complete determnistic finite automaton

## Usage

class Automaton
with fields:
* **graph**
  ```python
  graph = defaultdict(lambda: defaultdict(set))   
  ```
  * transitions (from, word) -> to
* **start**
  * start state

