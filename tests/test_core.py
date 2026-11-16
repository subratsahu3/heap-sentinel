import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from heap_sentinel.core import DifferentialMemoryTracker


class TestDifferentialMemoryTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = DifferentialMemoryTracker(window_size=5)

    def test_insufficient_samples(self):
        self.tracker.record_sample({"ConnectionPool": 10})
        self.assertIsNone(self.tracker.compute_velocity("ConnectionPool"))
        self.assertFalse(self.tracker.is_leaking("ConnectionPool"))

    def test_steady_state_zero_velocity(self):
        for _ in range(5):
            self.tracker.record_sample({"Buffer": 100})
        vel = self.tracker.compute_velocity("Buffer")
        self.assertEqual(vel, 0.0)
        self.assertFalse(self.tracker.is_leaking("Buffer"))

    def test_positive_leak_detection(self):
        # Emulate steady linear memory leak: 10, 25, 40, 55, 70
        for val in [10, 25, 40, 55, 70]:
            self.tracker.record_sample({"LeakySocket": val})

        vel = self.tracker.compute_velocity("LeakySocket")
        self.assertAlmostEqual(vel, 15.0)
        self.assertTrue(self.tracker.is_leaking("LeakySocket", velocity_threshold=10.0))
        self.assertFalse(self.tracker.is_leaking("LeakySocket", velocity_threshold=20.0))


if __name__ == "__main__":
    unittest.main()
