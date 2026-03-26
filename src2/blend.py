import numpy as np
import polyscope as ps
import warp as wp


# TODO: Add kernel params needed for one vertex's blending across all blendshapes.
@wp.kernel
def blend_kernel(
    base_verts: wp.array(dtype=wp.vec3),
    deltas: wp.array(dtype=wp.vec3),   # flattened (M*N)
    weights: wp.array(dtype=float),
    out_verts: wp.array(dtype=wp.vec3),
    num_verts: int,
    num_blendshapes: int,
):
    i = wp.tid()  # vertex index

    pos = base_verts[i]

    for j in range(num_blendshapes):
        idx = j * num_verts + i
        pos += weights[j] * deltas[idx]

    out_verts[i] = pos



class BlendState:
    """Manages internal data used for blending"""

    # TODO: Figure out what you need to get this running on Warp.
    def __init__(
        self,
        base_verts: np.ndarray,
        bs_deltas: np.ndarray,
        device,
        mesh_name: str,
        args,
    ):
        self.device = device
        self.mesh_name = mesh_name
        self.args = args

        self.num_blendshapes = bs_deltas.shape[0]
        self.num_verts = base_verts.shape[0]

        # Base vertices
        self.base_verts_dev = wp.array(
            base_verts.astype(np.float32),
            dtype=wp.vec3,
            device=device,
        )

        # Flatten deltas: (M, N, 3) → (M*N, 3)
        deltas_flat = bs_deltas.reshape(-1, 3).astype(np.float32)
        self.deltas_dev = wp.array(
            deltas_flat,
            dtype=wp.vec3,
            device=device,
        )

        # Weights
        self.weights_dev = wp.zeros(
            self.num_blendshapes,
            dtype=float,
            device=device,
        )

        # Output buffer
        self.out_verts_dev = wp.zeros(
            self.num_verts,
            dtype=wp.vec3,
            device=device,
        )


        self.frames_complete = 0
        self.profile_interval = 60

    # TODO
    def update(self, blend_weights: list[float]):
        """Launches Warp kernel (blend_kernel) and copies back blended vertices to polyscope"""
        should_print = self.args.profile and (
            self.frames_complete % self.profile_interval == 0
        )

        # HINT: Don't forget to copy CPU buffers to GPU beforehand...

        self.weights_dev = wp.array(
            np.array(blend_weights, dtype=np.float32),
            dtype=float,
            device=self.device,
        )

        with wp.ScopedTimer("blend_kernel_launch", print=should_print):
            # TODO: Populate inputs[] with your blend_kernel() args.
            wp.launch(
                blend_kernel,
                dim=self.num_verts,
                inputs=[
                    self.base_verts_dev,
                    self.deltas_dev,
                    self.weights_dev,
                    self.out_verts_dev,
                    self.num_verts,
                    self.num_blendshapes,
                ],
                device=self.device,
            )

        # .numpy() forces a barrier, but for sanity :)
        wp.synchronize()

        with wp.ScopedTimer("device_to_host_copy", print=should_print):
            blended_verts = self.out_verts_dev.numpy()

        with wp.ScopedTimer("update_polyscope_verts", print=should_print):
            ps.get_surface_mesh(self.mesh_name).update_vertex_positions(blended_verts)

        self.frames_complete += 1
