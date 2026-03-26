import numpy as np


# TODO
def catmullrom_spline_weights(u: float) -> np.ndarray:
    """
    Compute Catmull-Rom spline weights for parameter u
    Assumes u is clamped between [0, 1]

    See: https://en.wikipedia.org/wiki/Catmull%E2%80%93Rom_spline
    (note: they use t for interpolation parameter instead of u, which we used in spec)
    """

    u2 = u * u
    u3 = u2 * u

    c0 = 0.5 * (-u3 + 2*u2 - u)
    c1 = 0.5 * (3*u3 - 5*u2 + 2)
    c2 = 0.5 * (-3*u3 + 4*u2 + u)
    c3 = 0.5 * (u3 - u2)

    return np.array([c0, c1, c2, c3], dtype=np.float32)
