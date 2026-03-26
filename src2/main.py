from __future__ import annotations

from typing import Optional

import numpy as np
import polyscope as ps
import warp as wp

from blend import BlendState
from cli import parse_args
from interpolate import (
    make_catmullrom_callback,
    make_lerp_callback,
    make_slider_callback,
)
from utils import (
    build_expression_weights,
    load_blend_weights,
    load_custom_fbx_deltas,
    load_mesh,
)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)

    wp.init()
    if args.device is None:
        device = wp.get_preferred_device()
    else:
        device = wp.get_device(args.device)

    # Load blendshape deltas
    bs_deltas_by_name = load_custom_fbx_deltas("./data/base_deltas.txt")
    bs_names = list(bs_deltas_by_name.keys())
    bs_deltas = np.stack(list(bs_deltas_by_name.values()), axis=0)

    # Load expression weights
    expression_names = ["expression_smile", "expression_yell", "expression_sad", "expression_confused"]
    per_expression_weights = {
        name: load_blend_weights(f"./data/{name}_weights.txt") for name in expression_names
    }

    bs_weights = [0.0] * len(bs_names)

    # Load obj for polyscope rendering
    base_verts, faces = load_mesh("./data/base_mesh.obj")

    print(f"Base verts shape: {base_verts.shape}")
    print(f"Deltas shape: {bs_deltas.shape}")
    print(f"Num blendshapes: {bs_deltas.shape[0]}")
    print(f"Blendshape names: {bs_names}")

    # Initialize state in blend.py! See spec for explanation of BlendState.
    blender = BlendState(base_verts, bs_deltas, device, mesh_name="man", args=args)

    expression_order = ["base"] + expression_names
    expression_order, expression_weights = build_expression_weights(
        bs_names, per_expression_weights, expression_order=expression_order, include_base_expression=False
    )

    # Hacky, but use a list to make seconds_per_segment mutable in UI
    seconds_per_segment = [1.5]

    # Select one callback
    if args.mode == "slider":
        # TODO: Part 1 - Implement in interpolate.py!
        callback = make_slider_callback(blender, bs_names, bs_weights)
    elif args.mode == "lerp":
        # TODO: Part 2
        callback = make_lerp_callback(blender, expression_weights, seconds_per_segment)
    elif args.mode == "cmrom":
        # TODO: Part 2
        callback = make_catmullrom_callback(blender, expression_weights, seconds_per_segment)
    else:
        raise ValueError(f'Invalid callback chosen: "{args.mode}"')

    # Initialize polyscope
    ps.init()
    ps.set_up_dir("z_up")
    ps.register_surface_mesh("man", base_verts, faces, smooth_shade=True)

    # Set camera position and lookAt (Z-up coordinates)
    camera_position = (0.0, -0.5, 1.59)
    look_at_target = (0.0, 0.15, 1.59)
    ps.look_at(camera_position, look_at_target)

    ps.set_user_callback(callback)
    ps.show()

    return 0


if __name__ == "__main__":
    exit(main())
