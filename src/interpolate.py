from __future__ import annotations

import time
from typing import Callable

import numpy as np
import polyscope as ps

from spline import catmullrom_spline_weights


# TODO: e.g., bool changed = ps.imgui.SliderFloat(slider name, current value, min 0.0, max 1.0)
def make_slider_callback(
    blender, bs_names: list[str], bs_weights: list[float]
) -> Callable[[], None]:
    def callback() -> None: ...

    return callback


# TODO
def make_lerp_callback(
    blender,
    expression_weights: list[np.ndarray],
    seconds_per_segment: list[float],
) -> Callable[[], None]:
    start_time = time.perf_counter()

    def callback() -> None:
        # UI slider to control animation speed. Do not remove.
        changed = ps.imgui.SliderFloat(
            "Seconds per segment", seconds_per_segment[0], 0.1, 5.0
        )
        if changed[0]:
            seconds_per_segment[0] = changed[1]

        num_expressions = len(expression_weights)
        if num_expressions < 2:
            raise ValueError(f"Lerp requires at least 2 expressions, got {num_expressions}")

        t_elapsed = time.perf_counter() - start_time

        # TODO: complete the callback

    return callback


# TODO
def make_catmullrom_callback(
    blender,
    expression_weights: list[np.ndarray],
    seconds_per_segment: list[float],
) -> Callable[[], None]:
    start_time = time.perf_counter()

    def callback() -> None:
        # UI slider to control animation speed. Do not remove.
        changed = ps.imgui.SliderFloat(
            "Seconds per segment", seconds_per_segment[0], 0.1, 5.0
        )
        if changed[0]:
            seconds_per_segment[0] = changed[1]

        num_expressions = len(expression_weights)
        if num_expressions < 4:
            raise ValueError(f"Catmull-Rom requires at least 4 expressions, got {num_expressions}")

        t_elapsed = time.perf_counter() - start_time

        # TODO: complete the callback

    return callback
