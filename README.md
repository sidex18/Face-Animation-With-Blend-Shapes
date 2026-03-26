# Face Animation with Blend Shapes - UBC CPSC 426 Assignment 





## Running

```py
python .\src\main.py --mode slider
```

The options for `--mode` to be one of `slider`, `lerp`, and `cmrom`.

lerp and cmrom blend facial expressions using the linear interpolation and catmull rom splines, and sliders give control over different facial blendshapes

Take a look at `src/cli.py` for additional flags.

'src2' contains smooth blending for facial expressions without the 'slider' mode

# Visualization

## Polyscope

[Polyscope](https://polyscope.run/py) is the viewer used to visualize your mesh and interact with blend shapes.

**Camera controls:**




<p align="center" width="100%">
<video src="https://github.com/sidex18/Face-Animation-With-Blend-Shapes/blob/main/Blend%20Shapes%20catmull-rom.mp4" width="80%" controls></video>
</p>
- **Rotate**: Left-click and drag
- **Pan**: Shift + left-click and drag
- **Zoom**: Scroll wheel

You can also toggle mesh visibility, change rendering style (smooth/flat/wireframe), and adjust colors from the Polyscope structure options on the left panel.


