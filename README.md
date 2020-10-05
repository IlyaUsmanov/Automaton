# automaton

Converts your automaton to minimal complete determnistic finite automaton

## Usage

class Automaton
with fields:
	* **graph**
	  ```python
	  graph = defaultdict(lambda: defaultdict(set))   
	  ```
	  transitions (from, word) -> to
	* **start**
	  ```python
	  start = 0
	  ```
	  start state
	* **finish**
	  ```python
	  finish = set()
	  ```
	  a set of accept states
	* **states**
	  ```python
	  states = set()
	  ```
	  a finite set of states
	and methods:

