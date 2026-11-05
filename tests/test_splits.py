import unittest
from src.dataset import window_starts
class SplitTests(unittest.TestCase):
 def test_complete_windows_and_disjoint_phases(self):
  train=window_starts('train',250,1250,1250,250)
  val=window_starts('validation',250,1250,1250,250)
  test=window_starts('test',250,1250,1250,1250)
  self.assertTrue(train and val and test)
  self.assertTrue(all(100*250 <= i-1250 and i+1250<=400*250 for i in train+val+test))
  train_phase={j%(25000) for i in train for j in range(i-1250,i+1250)}
  val_phase={j%(25000) for i in val for j in range(i-1250,i+1250)}
  self.assertFalse(train_phase & val_phase)
 def test_unknown_split_fails(self):
  with self.assertRaises(ValueError): window_starts('other',250,1250,1250,250)
