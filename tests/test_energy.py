import unittest
import numpy as np
from src.energy import features,fit_ridge,predict_ridge
class EnergyTests(unittest.TestCase):
 def test_zero_inputs_are_finite(self):
  self.assertTrue(np.isfinite(features(np.zeros((1250,3)),np.zeros((1250,1)))).all())
 def test_log_scale_change(self):
  rng=np.random.default_rng(10);h=rng.normal(size=(1250,3));r=rng.normal(size=(1250,1))
  np.testing.assert_allclose(features(h*2,r*2)-features(h,r),np.log(2),atol=1e-10)
 def test_regression_on_known_log_linear_rule(self):
  rng=np.random.default_rng(11);x=rng.normal(size=(100,3));y=1+2*x[:,0]-3*x[:,1]
  m=fit_ridge(x[:80],y[:80],0)
  np.testing.assert_allclose(predict_ridge(m,x[80:]),y[80:],atol=1e-10)
