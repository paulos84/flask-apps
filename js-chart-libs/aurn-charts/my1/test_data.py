import unittest
from app2 import chart_data


class TestChartData(unittest.TestCase):

    def setUp(self):
        self.data = chart_data('no2', 'abd', 1000)

    def test_time(self):
        self.times = self.data[0]
        self.assertEqual(self.times[0], "23/09/2017 10:00:00")

    def test_first_value(self):
        self.values = self.data[1]
        self.assertEqual(self.values[0], 19)

    def test_non_values(self):
        self.no_data = chart_data('so2', 'abd', 1000)
        self.no_values = self.no_data[1]
        self.assertEqual(self.no_values[0], '')


if __name__ == '__main__':
    unittest.main()