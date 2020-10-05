import unittest
from automaton import Automaton
import sys, os

#other tests in progress
class Test(unittest.TestCase):
    def testDetermine(self):
        my_automaton = Automaton()
        my_automaton.add_edge(0, 1, '')
        my_automaton.add_edge(0, 1, 'a')
        my_automaton.add_edge(0, 1, 'b')
        my_automaton.add_edge(0, 0, 'ab')
        my_automaton.add_edge(0, 0, 'ba')
        my_automaton.add_finish(1)
        my_automaton.make_full_deterministic()
        
        self.assertTrue(my_automaton.in_language(''))
        self.assertTrue(my_automaton.in_language('a'))
        self.assertTrue(my_automaton.in_language('b'))
        self.assertTrue(my_automaton.in_language('ab' * 50))
        self.assertTrue(my_automaton.in_language('abba' * 50))
        self.assertFalse(my_automaton.in_language('bb'))
        self.assertFalse(my_automaton.in_language('abaa'))
    def testMinimize(self):
        my_automaton = Automaton()
        my_automaton.add_edge(0, 1, 'a')
        my_automaton.add_edge(1, 3, 'a')
        my_automaton.add_edge(0, 2, 'b')
        my_automaton.add_edge(2, 3, 'a')
        my_automaton.add_finish(3)
        my_automaton.minimize()

        self.assertEqual(len(my_automaton.states), 4)

        self.assertFalse(my_automaton.in_language(''))
        self.assertTrue(my_automaton.in_language('aa'))
        self.assertTrue(my_automaton.in_language('ba'))
        self.assertFalse(my_automaton.in_language('a'))
        self.assertFalse(my_automaton.in_language('b'))
