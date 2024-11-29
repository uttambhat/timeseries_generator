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

    def reproduce(
        self,
        dtime: float,
        custom_parameters: dict = {}
    ):
        if self.alive and self.fertility > 0.0:
            if np.random.binomial(1, self.fertility * dtime):
                if "location" not in custom_parameters.keys():
                    custom_parameters["location"] = self.location
                if "velocity" not in custom_parameters.keys():
                    custom_parameters["velocity"] = self.velocity
                if "acceleration" not in custom_parameters.keys():
                    custom_parameters["acceleration"] = self.acceleration
                if "diffusion_parameter" not in custom_parameters.keys():
                    custom_parameters["diffusion_parameter"] = self.diffusion_parameter
                if "diffusion_quantity" not in custom_parameters.keys():
                    custom_parameters["diffusion_quantity"] = self.diffusion_quantity
                if "weight" not in custom_parameters.keys():
                    custom_parameters["weight"] = self.weight
                if "fertility" not in custom_parameters.keys():
                    custom_parameters["fertility"] = self.fertility
                if "mortality" not in custom_parameters.keys():
                    custom_parameters["mortality"] = self.mortality
                return Particle(
                    location=custom_parameters["location"],
                    velocity = custom_parameters["velocity"],
                    acceleration = custom_parameters["acceleration"],
                    diffusion_parameter = custom_parameters["diffusion_parameter"],
                    diffusion_quantity = custom_parameters["diffusion_quantity"],
                    weight = custom_parameters["weight"],
                    fertility = custom_parameters["fertility"],
                    mortality = custom_parameters["mortality"]
                )
            else:
                return None

    def survive(self, dtime: float):
        if self.alive:
            if np.random.binomial(1, self.mortality * dtime):
                self.alive = False
                return False
            else:
                return True
        else:
            raise Exception("Particle is already dead!")
