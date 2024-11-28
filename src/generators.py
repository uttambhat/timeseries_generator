import numpy as np
from dataclasses import dataclass

@dataclass
class Spatiotemporal:
    """
    This class generates timeseries from the user-defined Spatiotemporal process. The process maybe discrete or
    continuous time and space. The process could be containing some or all elements of a reaction-advection-diffusion
    dynamics
    """