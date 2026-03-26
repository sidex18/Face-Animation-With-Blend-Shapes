from __future__ import annotations

import argparse
from typing import Optional


def parse_args(argv: Optional[list[str]] = None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        type=str,
        choices=["slider", "lerp", "cmrom"],
        default="slider",
        help="Animation mode: slider (manual control), lerp (linear interpolation), or cmrom (Catmull-Rom spline)",
    )
    parser.add_argument(
        "--device", type=str, default=None, help="Warp device, e.g. 'cuda:0' or 'cpu'"
    )
    parser.add_argument(
        "--profile",
        action="store_true",
        help="If you want to see profiling results (warp scoped timer info)",
    )
    args = parser.parse_args(argv)
    return args
