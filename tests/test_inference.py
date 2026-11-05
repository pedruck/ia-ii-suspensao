import unittest
import numpy as np
from src.inference import predict
class InferenceTests(unittest.TestCase):
 def test_invalid_input_rejected_before_loading_weights(self):
  with self.assertRaises(ValueError):predict('missing.pt',np.zeros((10,3)),np.zeros((10,1)))
  with self.assertRaises(ValueError):predict('missing.pt',np.full((1250,3),np.nan),np.zeros((1250,1)))
