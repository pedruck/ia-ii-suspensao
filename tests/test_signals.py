import unittest
import numpy as np
from src.signals import acceleration, wk_gain, weighted_rms, dominant_frequency

class SignalTests(unittest.TestCase):
    def test_sinusoidal_acceleration(self):
        fs=1000; t=np.arange(30000)/fs; f=2.; amp=.001
        a=acceleration(amp*np.sin(2*np.pi*f*t),fs)
        self.assertLess(abs(np.sqrt(np.mean(a[5000:]**2))/(amp*(2*np.pi*f)**2/np.sqrt(2))-1),.02)
    def test_published_wk_weights(self):
        # ISO reference weights reproduced in Vasquez, Appendix A.4.2.
        for f,gain in [(3.15,.804),(12.5,.902),(50,.246)]:
            self.assertLess(abs(wk_gain(f)/gain-1),.02)
    def test_weighted_sine_rms(self):
        fs=1000; f=4; t=np.arange(30000)/fs
        self.assertLess(abs(weighted_rms(np.sin(2*np.pi*f*t),fs,start=5000)/(wk_gain(f)/np.sqrt(2))-1),.02)
    def test_frequency_and_quiet_signal(self):
        fs=250; t=np.arange(1250)/fs
        self.assertAlmostEqual(dominant_frequency(np.sin(2*np.pi*2*t),fs),2)
        self.assertTrue(np.isnan(dominant_frequency(np.zeros(1250),fs)))
