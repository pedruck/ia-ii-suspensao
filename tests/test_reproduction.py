import unittest
from src.reproduction import compare_evaluations
class ReproductionTests(unittest.TestCase):
 def test_small_roundoff_is_accepted(self):
  r={'experiment':'all','method':'LSTM','seed':42,'class':'ALL','body_rmse_m':.001,'aw_mae':.1,'accuracy':.9}
  self.assertTrue(compare_evaluations([r],[r|{'body_rmse_m':.00100000001}])['matches_within_tolerance'])
 def test_changed_classification_or_missing_runs_fail(self):
  r={'experiment':'all','method':'LSTM','seed':42,'class':'ALL','body_rmse_m':.001,'aw_mae':.1,'accuracy':.9}
  self.assertFalse(compare_evaluations([r],[r|{'accuracy':.8}])['matches_within_tolerance'])
  self.assertFalse(compare_evaluations([r],[])['matches_within_tolerance'])
