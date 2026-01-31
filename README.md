# Assignment 2: Face Animation with Blend Shapes

Please start by reading the spec [A2.pdf](A2.pdf).

## [Name] [Student Number] [CWL Username]

**Collaborators:** [Names of people you discussed the assignment with, or N/A]

**References:** [Websites or resources you used, or N/A]

**AI Tools:** [Names of generative AI tools used (e.g. ChatGPT, Claude), or N/A]

**Feature Extension:** [Brief description of your Part III extension]

**Notes for grader:** [Any additional information, or N/A]

# Environment Setup

You are free to use whatever package / environment tools you would like.

That said, we are using `conda` for its popularity. You can grab miniconda3, a minimal version [here](https://www.anaconda.com/docs/getting-started/miniconda/install#quickstart-install-instructions).

## Creating Conda Environment

**NOTE**: Installing Polyscope takes some time. If you already have `cpsc426` from A1, just run:

```sh
conda activate cpsc426
pip install polyscope
```

Otherwise, create the environment with the following in your terminal:

```sh
conda create -n cpsc426 -c conda-forge --override-channels python=3.14.2 numpy pip openusd -y
conda activate cpsc426
pip install warp-lang polyscope
```

Run `conda activate cpsc426` every time you open a new shell intended to run the code.

## Running

```py
python .\src\main.py --mode slider
```

As you progress through the assignment, you will change `--mode` to be one of `slider`, `lerp`, and `cmrom`.

Take a look at `src/cli.py` for additional flags.

# Visualization

## Polyscope

[Polyscope](https://polyscope.run/py) is the viewer used to visualize your mesh and interact with blend shapes.

**Camera controls:**
- **Rotate**: Left-click and drag
- **Pan**: Shift + left-click and drag
- **Zoom**: Scroll wheel

You can also toggle mesh visibility, change rendering style (smooth/flat/wireframe), and adjust colors from the Polyscope structure options on the left panel.

## Comparing to Blender

If you would like to compare your results, you can import the original `.fbx` data into [Blender](https://www.blender.org/download/) to see what dragging given blendshapes **should** look like.

From there you can compare to Polyscope.

1. Install Blender
2. Open a new file / environment
3. Select and delete the default cube
4. Import with `File > Import > FBX (.fbx)`
