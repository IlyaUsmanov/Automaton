import unittest
from filecmp import cmp
from automaton import Automaton


# other tests in progress
class Test(unittest.TestCase):
    def testPrint(self):
        my_automaton = Automaton()
        my_automaton.add_edge(0, 1, '')
        my_automaton.add_edge(0, 1, 'a')
        my_automaton.add_edge(0, 1, 'b')
        my_automaton.add_edge(0, 0, 'ab')
        my_automaton.add_edge(0, 0, 'ba')
        my_automaton.add_finish(1)
        with open('my_output.txt', 'w') as output_file:
            my_automaton.print(output_file)

        self.assertTrue(cmp('my_output.txt', 'correct_output.txt'))

    def testDetermine(self):
        my_automaton = Automaton()
        my_automaton.add_edge(0, 1, '')
        my_automaton.add_edge(0, 1, 'a')
        my_automaton.add_edge(0, 1, 'b')
        my_automaton.add_edge(0, 0, 'ab')
        my_automaton.add_edge(0, 0, 'ba')
        my_automaton.add_edge(0, 2, '')
        my_automaton.add_edge(2, 0, '')
        my_automaton.add_finish(1)
        my_automaton.make_complete_deterministic()

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
