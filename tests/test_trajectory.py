import unittest
import numpy as np
from src.trajectory import trajectory_errors


class TrajectoryTests(unittest.TestCase):
    def test_prefix_errors_and_derived_stroke(self):
        true = np.zeros((2, 1250, 3))
        pred = true.copy()
        pred[:, 25:, 0] = .002
        pred[:, :, 1] = .001
        early = trajectory_errors(true, pred, .1)
        full = trajectory_errors(true, pred, 5)
        self.assertEqual(early['body_rmse_mm'], 0)
        self.assertAlmostEqual(early['wheel_rmse_mm'], 1)
        self.assertAlmostEqual(early['stroke_rmse_mm'], 1)
        self.assertAlmostEqual(full['body_rmse_mm'], 2 * np.sqrt(1225/1250))
        # Difference of predicted signals, rather than difference of their RMSEs.
        self.assertAlmostEqual(full['stroke_rmse_mm'], 1)

    def test_rejects_invalid_inputs(self):
        a = np.zeros((1, 1250, 3))
        for h in [0, -.1, 6, .101]:
            with self.assertRaises(ValueError):
                trajectory_errors(a, a, h)
        with self.assertRaises(ValueError):
            trajectory_errors(a, a[:, :-1], 5)
        with self.assertRaises(ValueError):
            trajectory_errors(a, a + np.nan, 5)
