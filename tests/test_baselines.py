import unittest
import numpy as np
from src.baselines import arx_predict
class BaselineTests(unittest.TestCase):
 def test_recursive_rollout_on_known_system(self):
  coef=np.zeros((8,3));coef[4,0]=.9;coef[6,0]=.1
  coef[5,1]=.8;coef[6,1]=.2
  history=np.zeros((2,3));history[-1,1:]=1
  pred=arx_predict(history,np.zeros(4),coef,lags=2)
  np.testing.assert_allclose(pred[:,0],.9**np.arange(1,5))
  np.testing.assert_allclose(pred[:,1],.8**np.arange(1,5))
