import unittest
from src.grouping import collapse_by_phase
class GroupingTests(unittest.TestCase):
 def test_repeated_passes_are_collapsed_without_merging_seeds(self):
  rows=[{'experiment':'all','method':'ridge','seed':0,'class':'C','phase_sample':100,'repetition':p,'aw_true':p,'aw_pred':p+1} for p in [2,3,4]]
  rows.append(rows[0]|{'seed':42})
  result=collapse_by_phase(rows)
  self.assertEqual(len(result),2)
  first=next(r for r in result if r['seed']==0)
  self.assertEqual(first['aw_true'],3)
  self.assertEqual(first['aw_pred'],4)
  self.assertEqual(first['passes'],3)
