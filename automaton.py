from collections import defaultdict
from queue import Queue
from tools import powerset
from sys import stdout


class Automaton:
    alphabet = ['a', 'b']

    def __init__(self, origin=None, start=0):
        if origin is None:
            self.graph = defaultdict(lambda: defaultdict(set))
            self.start = start
            self.finish = set()
            self.states = set()
        else:
            self._copy(origin)

    def _copy(self, origin):
        self.graph = defaultdict(lambda: defaultdict(set))
        for vertex in origin.graph:
            for word in origin.graph[vertex]:
                self.graph[vertex][word] = origin.graph[vertex][word].copy()
        self.start = origin.start
        self.finish = origin.finish.copy()
        self.states = origin.states.copy()

    def add_edge(self, vertex, to, word):
        self.graph[vertex][word].add(to)
        self.states.add(vertex)
        self.states.add(to)

    def add_finish(self, vertex):
        self.finish.add(vertex)

    def _delete_vertexes(self):
        queue = Queue()
        queue.put(self.start)
        free = self.states.copy()
        free.remove(self.start)
        while not queue.empty():
            vertex = queue.get()
            for word in self.graph[vertex]:
                for to in self.graph[vertex][word]:
                    if to in free:
                        free.remove(to)
                        queue.put(to)
        for vertex in free:
            self.graph.pop(vertex, None)
            self.finish.discard(vertex)
            self.states.remove(vertex)

    def _split_big_word(self, vertex, word, to):
        last = vertex
        for letter in word[:-1]:
            new_vertex = max(self.states) + 1
            self.states.add(new_vertex)
            self.graph[last][letter].add(new_vertex)
            last = new_vertex
        self.graph[last][word[-1]].add(to)

    def _delete_big_words(self):
        tmp_automaton = Automaton(self)
        for vertex in self.graph:
            for word in self.graph[vertex]:
                if len(word) > 1:
                    for to in self.graph[vertex][word]:
                        tmp_automaton._split_big_word(vertex, word, to)
                    tmp_automaton.graph[vertex].pop(word, 0)
        self._copy(tmp_automaton)

    def _replace_epsilon_edges(self, vertex, current, used=None):
        if used is None:
            used = {vertex}
        if current in used:
            return
        used.add(current)
        if (current in self.finish):
            self.finish.add(vertex)
        for word in self.graph[current]:
            for next_vertex in self.graph[current][word]:
                if word == '':
                    self._replace_epsilon_edges(vertex, next_vertex, used)
                else:
                    self.graph[vertex][word].add(next_vertex)

    def _delete_epsilons(self):
        tmp_automaton = Automaton(self)
        for vertex in self.graph:
            for current in self.graph[vertex]['']:
                tmp_automaton._replace_epsilon_edges(vertex, current)
            tmp_automaton.graph[vertex].pop('', None)
        self._copy(tmp_automaton)

    def _delete_multi_edges(self):
        new_automaton = Automaton(start=2 ** self.start)
        for subset in powerset(self.states):
            new_vertex = 0
            for old_vertex in subset:
                new_vertex |= 2 ** old_vertex
            new_automaton.states.add(new_vertex)
            for letter in Automaton.alphabet:
                new_neighbour = 0
                for old_vertex in subset:
                    for old_neighbour in self.graph[old_vertex][letter]:
                        new_neighbour |= 2 ** old_neighbour
                if new_neighbour != 0:
                    new_automaton.add_edge(new_vertex, new_neighbour, letter)
            if len(subset & self.finish) != 0:
                new_automaton.add_finish(new_vertex)
        self._copy(new_automaton)

    def determine(self):
        self._delete_big_words()
        self._delete_epsilons()
        self._delete_vertexes()
        self._delete_multi_edges()
        self._delete_vertexes()

    def go(self, vertex, letter):
        return list(self.graph[vertex][letter])[0]

    def make_complete_deterministic(self):
        self.determine()
        new_vertex = max(self.states) + 1
        self.states.add(new_vertex)
        for vertex in self.states:
            for letter in Automaton.alphabet:
                if len(self.graph[vertex][letter]) == 0:
                    self.graph[vertex][letter].add(new_vertex)

    def _split_by_groups(self):
        colors = {vertex: int(vertex in self.finish) for vertex in self.states}
        changed = True
        while changed:
            groups = defaultdict(set)
            for vertex in self.states:
                key = [colors[vertex]]
                for letter in Automaton.alphabet:
                    neighbour = self.go(vertex, letter)
                    key.append(colors[neighbour])
                key = tuple(key)
                groups[key].add(vertex)
            changed = (max(colors.values()) + 1 != len(groups))
            for (color, group) in enumerate(groups.values()):
                for vertex in group:
                    colors[vertex] = color
        return colors

    def minimize(self):
        self.make_complete_deterministic()
        colors = self._split_by_groups()
        new_automaton = Automaton(start=colors[self.start])
        for vertex in self.states:
            for letter in Automaton.alphabet:
                to = self.go(vertex, letter)
                new_automaton.add_edge(colors[vertex], colors[to], letter)
            if vertex in self.finish:
                new_automaton.add_finish(colors[vertex])
            new_automaton.states.add(colors[vertex])
        self._copy(new_automaton)
        self._delete_vertexes()

    def print(self, output=stdout):
        for vertex in self.states:
            for word in self.graph[vertex]:
                for to in self.graph[vertex][word]:
                    print('(', vertex, ',', word, ') ->', to, file=output)
        print('start:', self.start, file=output)
        for vertex in self.finish:
            print(vertex, file=output)

    def in_language(self, word):
        vertex = self.start
        for letter in word:
            vertex = self.go(vertex, letter)
        return vertex in self.finish
