import numpy as np
import polyscope as ps
import warp as wp


# TODO: Add kernel params needed for one vertex's blending across all blendshapes.
@wp.kernel
def blend_kernel(
    # Add your params here
    ):
    # HINT: You probably want an output buffer for the updated vertices.
    #       When you are done, be sure to update the wp.launch(...) inputs below!
    ...


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
        self.frames_complete = 0
        self.profile_interval = 60

    # TODO
    def update(self, blend_weights: list[float]):
        """Launches Warp kernel (blend_kernel) and copies back blended vertices to polyscope"""
        should_print = self.args.profile and (
            self.frames_complete % self.profile_interval == 0
        )

        # HINT: Don't forget to copy CPU buffers to GPU beforehand...

        with wp.ScopedTimer("blend_kernel_launch", print=should_print):
            # TODO: Populate inputs[] with your blend_kernel() args.
            wp.launch(
                blend_kernel,
                dim=self.num_verts,
                inputs=[...],
                device=self.device,
            )

        # .numpy() forces a barrier, but for sanity :)
        wp.synchronize()

        with wp.ScopedTimer("device_to_host_copy", print=should_print):
            blended_verts = ...

        with wp.ScopedTimer("update_polyscope_verts", print=should_print):
            ps.get_surface_mesh(self.mesh_name).update_vertex_positions(blended_verts)

        self.frames_complete += 1
