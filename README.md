# Automaton

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
* **add_edge(*from_vertex, to_vertex, word*)**
  * add edge from from_vertex to to_vertex by word
* **add_finish(*vertex*)**
  * add state vertex to set of finish states
* **determine**()
  * convert automaton to deterministic
* **make_full_deterministic**()
  * convert automaton to complete deterministic
* **minimize**()
  * convert automaton to minimal complete deterministic
* **print**()
  * print your automaton in readable format

## Example


The following code converts automaton to deterministic automaton
```python
from automaton import Automaton

my_automaton = Automaton()
my_automaton.add_edge(0, 1, '')
my_automaton.add_edge(0, 1, 'a')
my_automaton.add_edge(0, 1, 'b')
my_automaton.add_edge(0, 0, 'ab')
my_automaton.add_edge(0, 0, 'ba')
my_automaton.add_finish(1)
my_automaton.determine()
my_automaton.print()
```

Output:
```
( 1 , a ) -> 6
( 1 , b ) -> 10
( 6 , b ) -> 1
( 10 , a ) -> 1
start: 1
1
6
10
```
the last numbers are numbers of finish states

To run tests execute the following bash code in the repo directory:
```shell
coverage run -m unittest discover
coverage html
open htmlcov/index.html
```
