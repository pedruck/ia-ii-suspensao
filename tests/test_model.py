import unittest
import torch
from src.model import SuspensionLSTM
class ModelTests(unittest.TestCase):
 def test_variable_batch_and_horizon(self):
  model=SuspensionLSTM(8)
  for batch in [1,3]:
   result,log_aw=model(torch.zeros(batch,20,3),torch.zeros(batch,12,1))
   self.assertEqual(tuple(result.shape),(batch,12,3))
   self.assertEqual(tuple(log_aw.shape),(batch,))
   self.assertTrue(torch.isfinite(result).all())
   (result.sum()+log_aw.sum()).backward()
   self.assertTrue(all(p.grad is not None for p in model.parameters()))
