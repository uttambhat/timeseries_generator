"""
This contains classes to generate timeseries from the user-defined Spatiotemporal process. The process maybe discrete or
continuous time and space. The process could be containing some or all elements of a reaction-advection-diffusion
dynamics
"""
from typing import Optional, Union

import numpy as np
from dataclasses import dataclass

@dataclass
class Particle:
    location: np.ndarray
    velocity: Optional[np.ndarray] = None
    acceleration: Optional[np.ndarray] = None
    diffusion_parameter: Union[float, np.ndarray] = 1.0
    diffusion_quantity: str = "location"
    weight: float = 1.0
    fertility: float = 0.0
    mortality: float = 0.0
    """
    A particle class.

    Attributes
    ----------
    location: np.ndarray
    velocity: Optional[np.ndarray]
    acceleration: Optional[np.ndarray]
    diffusion_parameter: Union[float, any] = 1.0
    weight: float = 1.0
    fertility: float = 0.0
    mortality: float = 0.0
    
    """
        
    def __post_init__(self):
        self.dimension = len(self.location)
        if self.velocity is None:
            self.velocity = np.zeros(self.dimension)
        if self.acceleration is None:
            self.acceleration = np.zeros(self.dimension)
        if isinstance(self.diffusion_parameter, float):
            self.diffusion_parameter = np.ones(self.dimension) * self.diffusion_parameter
        self.alive = True

    def move(self, dtime: float):
        if self.alive:
            if self.diffusion_quantity == "location":
                self.location = self.location + np.random.normal(0.0, np.sqrt(self.diffusion_parameter * dtime))
            elif self.diffusion_quantity == "velocity":
                self.velocity = self.velocity + np.random.normal(0.0, np.sqrt(self.diffusion_parameter * dtime))
            elif self.diffusion_quantity == "acceleration":
                self.acceleration = self.acceleration + np.random.normal(0.0, np.sqrt(self.diffusion_parameter * dtime))
            self.velocity = self.velocity + dtime * self.acceleration
            self.location = self.location + dtime * self.velocity
        else:
            raise Exception("Particle is dead!")

    def reproduce(self, dtime: float):
        if self.alive:
            if np.random.binomial(1, self.fertility * dtime):
                return Particle(
                    location=self.location,
                    velocity = self.velocity,
                    acceleration = self.acceleration,
                    diffusion_parameter = self.diffusion_parameter,
                    diffusion_quantity = self.diffusion_quantity,
                    weight = self.weight,
                    fertility = self.fertility,
                    mortality = self.mortality
                )
            else:
                return None
        else:
            raise Exception("Particle is dead!")

    def survive(self, dtime: float):
        if self.alive:
            if np.random.binomial(1, self.mortality * dtime):
                self.alive = False
                return False
            else:
                return True
        else:
            raise Exception("Particle is already dead!")
