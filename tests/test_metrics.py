import unittest
from src.metrics import classification
class MetricsTests(unittest.TestCase):
 def test_confusion_and_balanced_accuracy(self):
  r=classification([0,0,1,1],[0,1,0,1])
  self.assertEqual(r['confusion'],[[1,1],[1,1]])
  self.assertEqual(r['balanced_accuracy'],.5)
  self.assertEqual(r['macro_f1'],.5)
 def test_single_class_is_not_discrimination(self):
  r=classification([1,1],[1,1])
  self.assertIsNone(r['balanced_accuracy'])
  self.assertIsNone(r['macro_f1'])
  self.assertEqual(r['recall_discomfort'],1)
