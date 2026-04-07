import unittest

from easyclicker.interval import parse_interval


class ParseIntervalTests(unittest.TestCase):
    def test_microseconds(self):
        interval = parse_interval(10, "microseconds")
        self.assertAlmostEqual(interval.seconds, 0.00001)

    def test_hours(self):
        interval = parse_interval(2, "hours")
        self.assertEqual(interval.seconds, 7200)

    def test_invalid_unit(self):
        with self.assertRaises(ValueError):
            parse_interval(1, "days")

    def test_non_positive(self):
        with self.assertRaises(ValueError):
            parse_interval(0, "seconds")


if __name__ == "__main__":
    unittest.main()
