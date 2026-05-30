from typing import Protocol

import numpy as np


class Distribution(Protocol):
    def sample(self, mean: float, sd: float): ...


class Normal(Distribution):
    def sample(self, mean: float, sd: float):
        rng = np.random.default_rng()
        num = rng.normal(loc=mean, scale=sd, size=None)
        return num
