from typing import Protocol

import numpy as np


class Distribution(Protocol):
    def sample(self) -> float: ...


class Normal(Distribution):
    def __init__(
        self, rng: np.random.Generator, mean: float = 1.0, sd: float = 0.25
    ) -> None:
        self.rng = rng
        self.mean = mean
        self.sd = sd

    def sample(self) -> float:
        return self.rng.normal(loc=self.mean, scale=self.sd, size=None)


class Exponential(Distribution):
    def __init__(self, rng: np.random.Generator, scale: float = 1.0) -> None:
        self.rng = rng
        self.scale = scale

    def sample(self) -> float:
        num = self.rng.exponential(scale=self.scale, size=None)
        return num


class LogNormal(Distribution):
    def __init__(
        self, rng: np.random.Generator, mean: float = 0, sigma: float = 0.4
    ) -> None:
        self.rng = rng
        self.mean = mean
        self.sigma = sigma

    def sample(self) -> float:
        num = self.rng.lognormal(mean=self.mean, sigma=self.sigma, size=None)
        return num
