import unittest
import numpy as np
from src.inference import predict
from src.inference import load_trajectory_model
from src.model import SuspensionLSTM
import tempfile
import torch
class InferenceTests(unittest.TestCase):
 def test_audited_joint_weights_and_rms_only_guard(self):
  with tempfile.NamedTemporaryFile(suffix='.pt') as f:
   model=SuspensionLSTM(4)
   ck={'state':model.state_dict(),'mode':'joint_120','seed':42,'mean':[0]*4,'std':[1]*4}
   torch.save(ck,f.name)
   loaded,_=load_trajectory_model(f.name)
   self.assertEqual(loaded.encoder.hidden_size,4)
   trajectory,result=predict(f.name,np.zeros((1250,3)),np.zeros((1250,1)))
   self.assertEqual(trajectory.shape,(1250,3))
   self.assertTrue(np.isfinite(result['weighted_rms_predicted']))
   ck['mode']='rms_only_120';torch.save(ck,f.name)
   with self.assertRaises(ValueError):load_trajectory_model(f.name)
 def test_invalid_input_rejected_before_loading_weights(self):
  with self.assertRaises(ValueError):predict('missing.pt',np.zeros((10,3)),np.zeros((10,1)))
  with self.assertRaises(ValueError):predict('missing.pt',np.full((1250,3),np.nan),np.zeros((1250,1)))
