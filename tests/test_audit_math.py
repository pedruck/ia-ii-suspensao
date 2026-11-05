import unittest
import numpy as np
from src.audit_math import independent_rms,svd_predict
from src.signals import weighted_rms
from src.energy import fit_ridge,predict_ridge
class AuditMathTests(unittest.TestCase):
 def test_rms_against_analytic_weight_and_original(self):
  t=np.arange(20000)/1000;a=np.sin(2*np.pi*3.15*t)
  self.assertLess(abs(independent_rms(a,1000)-.804/np.sqrt(2)),.01)
  rng=np.random.default_rng(87);a=rng.normal(size=1250)
  self.assertAlmostEqual(independent_rms(a,250),weighted_rms(a,250),places=12)
 def test_float32_archive_agrees_with_double_precision_audit(self):
  a=np.random.default_rng(89).normal(size=1250).astype("float32")
  self.assertLess(abs(independent_rms(a,250)-weighted_rms(a,250)),1e-7)
 def test_svd_matches_normal_equations(self):
  rng=np.random.default_rng(88);x=rng.normal(size=(100,8));y=rng.normal(size=100);v=rng.normal(size=(20,8))
  np.testing.assert_allclose(svd_predict(x,y,v,.1),predict_ridge(fit_ridge(x,y,.1),v),rtol=1e-10,atol=1e-10)
