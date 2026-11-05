"""Sequence model conditioned on known future road elevation."""
import torch
from torch import nn

class SuspensionLSTM(nn.Module):
    def __init__(self,hidden=64):
        super().__init__()
        self.encoder=nn.LSTM(3,hidden,batch_first=True)
        self.decoder=nn.LSTM(1,hidden,batch_first=True)
        self.output=nn.Linear(hidden,3)
        self.log_rms=nn.Linear(hidden,1)
    def forward(self,history,road_future):
        _,state=self.encoder(history)
        decoded,_=self.decoder(road_future,state)
        return self.output(decoded), self.log_rms(decoded.mean(dim=1)).squeeze(-1)
