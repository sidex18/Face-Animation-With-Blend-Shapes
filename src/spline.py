import numpy as np


# TODO
def catmullrom_spline_weights(u: float) -> np.ndarray:
    """
    Compute Catmull-Rom spline weights for parameter u
    Assumes u is clamped between [0, 1]

    See: https://en.wikipedia.org/wiki/Catmull%E2%80%93Rom_spline
    (note: they use t for interpolation parameter instead of u, which we used in spec)
    """

    return np.array()  # TODO: Replace with your updated weights!
