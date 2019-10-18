import unittest
from misc import round_list

class MyTestCase(unittest.TestCase):
    def test_round_list(self):

        self.assertEqual(round_list([0.3132131, 32.3213], 2), [0.31, 32.32])
        self.assertEqual(round_list([0.3132131, 32.3213], 0), [0, 32])


if __name__ == '__main__':
    unittest.main()
