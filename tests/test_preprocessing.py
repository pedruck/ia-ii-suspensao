import unittest
import numpy as np
from scipy.signal import butter,sosfilt
from src.preprocessing import prepare_signals

class PreprocessingTests(unittest.TestCase):
 def test_80hz_matches_original_pipeline(self):
  rng=np.random.default_rng(4);z=rng.normal(0,.001,(10000,3))
  centered=z-z[:5000].mean(0)
  a=sosfilt(butter(4,80,fs=1000,output='sos'),np.r_[0.,0.,np.diff(centered[:,1],n=2)]*1000**2)
  expected=sosfilt(butter(8,100,fs=1000,output='sos'),np.column_stack([centered,a]),axis=0)[::4].astype('float32')
  np.testing.assert_array_equal(prepare_signals(z,80),expected)
 def test_future_samples_do_not_change_past(self):
  rng=np.random.default_rng(5);z=rng.normal(size=(12000,3));other=z.copy();other[8000:]+=100
  np.testing.assert_array_equal(prepare_signals(z,60)[:2000],prepare_signals(other,60)[:2000])
 def test_sinusoidal_rms(self):
  from src.signals import weighted_rms,wk_gain
  t=np.arange(30000)/1000;z=np.column_stack([np.zeros(len(t)),.001*np.sin(2*np.pi*2*t),np.zeros(len(t))])
  for cutoff in [40,60,80]:
   a=prepare_signals(z,cutoff)[2500:,3]
   expected=.001*(2*np.pi*2)**2/np.sqrt(2)*wk_gain(2)
   self.assertLess(abs(weighted_rms(a,250)/expected-1),.02)
