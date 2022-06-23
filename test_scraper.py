import unittest
from scraper import a_sum

class TestSum(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(a_sum(), 2)

    def test_again(self):
        self.assertEqual(a_sum(), 4)

if __name__ == '__main__':
    unittest.main()