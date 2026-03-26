from __future__ import annotations

import time
from typing import Callable

import numpy as np
import polyscope as ps

from spline import catmullrom_spline_weights


def ease_in(u: float) -> float:
    return u * u

def ease_out(u: float) -> float:
    return 1.0 - (1.0 - u) * (1.0 - u)

def ease_in_out(u: float) -> float:
    if u < 0.5:
        return 2 * u * u
    else:
        return 1.0 - pow(-2.0 * u + 2.0, 2) / 2.0



# TODO: e.g., bool changed = ps.imgui.SliderFloat(slider name, current value, min 0.0, max 1.0)
def make_slider_callback(
    blender, bs_names: list[str], bs_weights: list[float]
) -> Callable[[], None]:
    def callback() -> None: 
        changed_any = False

        for i, name in enumerate(bs_names):
            changed = ps.imgui.SliderFloat(
                name, bs_weights[i], 0.0, 1.0
            )
            if changed[0]:
                bs_weights[i] = changed[1]
                changed_any = True

        if changed_any:
            blender.update(bs_weights)

    return callback


# TODO
def make_lerp_callback(
    blender,
    expression_weights: list[np.ndarray],
    seconds_per_segment: list[float],
) -> Callable[[], None]:
    start_time = time.perf_counter()
    use_ease = False   # ← state lives here

    def callback() -> None:
        nonlocal use_ease

        # UI controls
        changed, use_ease = ps.imgui.Checkbox("Ease In-Out", use_ease)

        changed = ps.imgui.SliderFloat(
            "Seconds per segment", seconds_per_segment[0], 0.1, 5.0
        )
        if changed[0]:
            seconds_per_segment[0] = changed[1]

        t_elapsed = time.perf_counter() - start_time
        s = seconds_per_segment[0]

        seg = int(t_elapsed // s) % len(expression_weights)
        u = (t_elapsed / s) % 1.0

        if use_ease:
            u = ease_in_out(u)

        w0 = expression_weights[seg]
        w1 = expression_weights[(seg + 1) % len(expression_weights)]
        w = (1.0 - u) * w0 + u * w1

        blender.update(w.tolist())

    return callback


# TODO
def make_catmullrom_callback(
    blender,
    expression_weights: list[np.ndarray],
    seconds_per_segment: list[float],
) -> Callable[[], None]:
    start_time = time.perf_counter()
    use_ease = False
    def callback() -> None:
        nonlocal use_ease
        # UI slider to control animation speed. Do not remove.

        changed, use_ease = ps.imgui.Checkbox("Ease In-Out", use_ease)
        changed = ps.imgui.SliderFloat(
            "Seconds per segment", seconds_per_segment[0], 0.1, 5.0
        )
        if changed[0]:
            seconds_per_segment[0] = changed[1]

        num_expressions = len(expression_weights)
        if num_expressions < 4:
            raise ValueError(f"Catmull-Rom requires at least 4 expressions, got {num_expressions}")

        t_elapsed = time.perf_counter() - start_time

        s = seconds_per_segment[0]

        seg = int(t_elapsed // s) % num_expressions
        u = (t_elapsed / s) % 1.0
        if use_ease:
            u = ease_in_out(u)

        p0 = expression_weights[(seg - 1) % num_expressions]
        p1 = expression_weights[seg]
        p2 = expression_weights[(seg + 1) % num_expressions]
        p3 = expression_weights[(seg + 2) % num_expressions]

        c = catmullrom_spline_weights(u)
        w = c[0]*p0 + c[1]*p1 + c[2]*p2 + c[3]*p3

        blender.update(w.tolist())

    return callback
