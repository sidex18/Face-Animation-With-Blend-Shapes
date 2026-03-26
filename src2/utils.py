from typing import Optional

import numpy as np


def load_mesh(filename: str) -> tuple[np.ndarray, np.ndarray]:
    """Load an OBJ file and return vertices and faces as numpy arrays."""
    verts = []
    faces = []

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("v "):
                # Vertex line: v x y z
                parts = line.split()
                verts.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith("f "):
                # Face line: f v1 v2 v3 (indices are 1-based in OBJ format)
                parts = line.split()
                # Handle faces with texture/normal indices (e.g., "f v1/vt1/vn1 v2/vt2/vn2 v3/vt3/vn3")
                face = []
                for part in parts[1:]:
                    # Extract just the vertex index (first number before any /)
                    vertex_idx = int(part.split("/")[0]) - 1
                    face.append(vertex_idx)
                faces.append(face)

    # Convert to numpy arrays
    verts = np.array(verts)
    faces = np.array(faces)

    return verts, faces


def load_custom_fbx_deltas(filename: str) -> dict[str, np.ndarray]:
    blendshape_deltas = {}

    with open(filename, "r") as f:
        # Each line is blendshape identifier <index_name> followed by <dx0 dy0 dz0 dx1 dy1 dz1 ... dxn-1 dyn-1 dzn-1>
        for line in f:
            line = line.strip()
            if line:
                parts = line.split()

                # First token is the blendshape name (if it exists, otherwise the index)
                name = parts[0]

                # Parse the rest as floats
                deltas_flattened = list(map(float, parts[1:]))

                # Reshape
                deltas_reshaped = np.array(deltas_flattened).reshape(-1, 3)
                blendshape_deltas[name] = deltas_reshaped

    return blendshape_deltas


def load_blend_weights(filename: str) -> dict[str, float]:
    """Given a file, e.g., expression_smile_weights.txt, will load and return {name : weight} pairs in a dictionary"""
    blendshape_weights = {}

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split()

                name = parts[0]
                wt = float(parts[1])

                blendshape_weights[name] = wt

    return blendshape_weights


def build_expression_weights(
    bs_names: list[str],
    per_expression_weights: dict[str, dict[str, float]],
    expression_order: Optional[list[str]] = None,
    include_base_expression: bool = False,
) -> tuple[list[str], list[np.ndarray]]:
    if expression_order is None:
        expression_order = sorted(per_expression_weights.keys())

    ordered_weights = []
    for expression_name in expression_order:
        weights = per_expression_weights.get(expression_name, {})
        ordered_weights.append(
            np.array([weights.get(name, 0.0) for name in bs_names], dtype=np.float32)
        )

    if include_base_expression:
        expression_order = list(expression_order) + ["base"]
        ordered_weights.append(np.zeros(len(bs_names), dtype=np.float32))

    return expression_order, ordered_weights
