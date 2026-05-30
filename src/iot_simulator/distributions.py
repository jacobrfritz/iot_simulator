from typing import Protocol

import numpy as np


class Distribution(Protocol):
    def sample(self)->float: ...


class Normal(Distribution):
    def __init__(self, mean: float = 0.1, sd: float = 0.01) -> None:
        self.rng = np.random.default_rng()
        self.mean = mean
        self.sd = sd
        
    def sample(self)->float:
        return self.rng.normal(loc=self.mean, scale=self.sd, size=None)
        

class Poisson(Distribution):
    def __init__(self, lam: float = 0.5) -> None:
        self.rng = np.random.default_rng()
        self.lam = lam
        
    def sample(self)->float:
        num = self.rng.poisson(lam=self.lam, size=None)
        return num
      
class LogNormal(Distribution):
    def __init__(self, mean: float = -3.0, sigma: float = 0.5) -> None:
        self.rng = np.random.default_rng()
        self.mean = mean
        self.sigma = sigma

    def sample(self)->float:
        num = self.rng.lognormal(mean=self.mean, sigma=self.sigma, size=None)
        return num
    

