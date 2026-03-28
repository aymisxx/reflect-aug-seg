# **Reflect-Aug-Seg** 📡🫧 (Preliminary Work Notebooks)

**Project theme:** Reflectivity-Augmented LiDAR Scene Understanding for Robotic Perception

This repository studies whether a simple range-aware transformation of LiDAR intensity can serve as a useful complementary cue for semantic scene understanding. The current stage is **preliminary work**, not a final deployable perception system. The aim here is to establish feasibility, inspect behavior honestly, and leave the heavier engineering and evaluation for the final phase.

The core proxy used throughout the preliminary work is:

$$
\hat{\rho} = I \cdot R
$$

where:

- $I$ is raw LiDAR intensity.
- $R$ is point-wise Euclidean range.
- $\hat{\rho}$ is a **pseudo-reflectivity** proxy, not true calibrated reflectivity.

That honesty clause matters. This project does **not** claim physical reflectance recovery yet.

---

# What this preliminary stage is trying to prove

The preliminary stage is designed to answer a restrained but meaningful question:

> If raw LiDAR intensity is range-entangled and only partially useful for semantic understanding, does a lightweight range-aware proxy like $I \cdot R$ expose more useful structure for scene interpretation?

In practical terms, the preliminary work tries to establish five things:

1. the SemanticKITTI loading and label pipeline is correct.
2. raw intensity and pseudo-reflectivity can be extracted and visualized cleanly.
3. the proxy behaves differently from raw intensity on a single frame.
4. the proxy remains stable enough over short motion windows to be worth taking seriously.
5. class-wise semantic patterns become at least modestly more interpretable under the proxy.

This is a **proof-of-promise**, not a final proof of robustness.

# Core concepts

## LiDAR point cloud

Each point from the sensor is represented as:

$$
p_i = (x_i, y_i, z_i, I_i)
$$

where $(x_i, y_i, z_i)$ are spatial coordinates and $I_i$ is recorded intensity.

## Range
For each point:

$$
R_i = \sqrt{x_i^2 + y_i^2 + z_i^2}
$$

## Raw intensity is not pure reflectivity
A simplified LiDAR return relationship is:

$$
I_i \propto \frac{\rho_i \cos(\alpha_i)}{R_i^2}
$$

where:

- $\rho_i$ is surface reflectivity.
- $\alpha_i$ is incidence angle.
- $R_i$ is range.

So raw intensity mixes together:

- surface behavior.
- distance effects.
- measurement geometry.

This means raw intensity is **not** the same thing as material or calibrated reflectivity.

## Pseudo-reflectivity proxy
Because full calibration terms are unavailable in this project scope, we use:

$$
\hat{\rho}_i = I_i \cdot R_i
$$

This is a heuristic range-aware feature. It is computationally cheap, easy to compute, and useful as a first research probe.

# Dataset used

The preliminary work uses **SemanticKITTI**, specifically **sequence 00** arranged under:

```text
reflect-aug-seg/
├── data
│   └── semantickitti_subset
│     └── dataset
│       └── sequences
│         └── 00                # Just one sequence for prelim.
│           ├── calib.txt
│           ├── labels
│           . ├── 000000.label
│           . ├── 000001.label
│           . ├── 000002.label
│           . ├── 000003.label
│           . .
│           . .
│           . .
│           . ├── 004539.label
│           . └── 004540.label
│           ├── poses.txt
│           └── velodyne
│           . ├── 000000.bin
│           . ├── 000001.bin
│           . ├── 000002.bin │
│           . .
│           . .
│           . .
│           . ├── 004539.bin
│           . └── 004540.bin
│           └── times.txt
│
├── requirements.txt
│
├── LICENSE                            # MIT
│
├── notebooks/                         # Preliminary Work
│   ├── artifacts/                     # GIF Plots
│   ├── 01_load_data.ipynb
│   ├── 02_single_frame_reflectivity_analysis.ipynb
│   ├── 03_multi_frame_reflectivity_over_motion.ipynb
│   ├── 04_single_frame_semantic_reflectivity_analysis.ipynb
│   └── 05_multi_frame_semantic_consistency.ipynb
│
├── src/                               # Future/Final Work              
│   ├── io/
│   │   └── loader.py
│   ├── features/
│   │   └── pseudo_reflectivity.py
│   ├── visualization/
│   │   ├── first_person.py
│   │   └── top_view.py
│   ├── temporal/
│   │   └── sequence_processor.py
│   └── semantics/
│       └── semantic_analysis.py
│
├── results/                            # Final Work
│
└── README.md
```

Expected files and folders inside `sequences/00`:

- `velodyne/`
- `labels/`
- `calib.txt`
- `poses.txt`
- `times.txt`

The notebooks assume they are run from the `notebooks/` directory, so the working dataset path becomes:

```python
Path("../data/semantickitti_subset/dataset/sequences/00")
```

The final-stage `src/` modular pipeline is intentionally left for later work.

# Environment setup

## Create a virtual environment
From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## Install dependencies
Assuming `requirements.txt` contains the notebook dependencies:

```bash
pip install -r requirements.txt
```

Typical packages needed for the current preliminary notebooks include:

```text
numpy
pandas
matplotlib
jupyter
notebook
ipykernel
imageio
scipy
```

If GIF rendering is included, `imageio` is required.

## Start Jupyter
From the repository root:

```bash
jupyter notebook
```

Then open the `notebooks/` folder and run the notebooks **in order**.

# Dataset placement procedure

## Step 1: Download SemanticKITTI data
Download the required SemanticKITTI sequence data and labels (Total **~84 GB**).

## Step 2: Place the files in the correct folder
The final folder should look like:

```text
data/semantickitti_subset/dataset/sequences/00/
├── calib.txt
├── poses.txt
├── times.txt
├── velodyne/
│   ├── 000000.bin
│   ├── 000001.bin
│   └── ...
└── labels/
    ├── 000000.label
    ├── 000001.label
    └── ...
```

## Step 3: Verify structure before analysis
Notebook 01 checks that all expected folders and files exist before loading any data.

# How to run the preliminary notebooks

Run them in sequence, because each one is the next boss battle in the research staircase.

## Notebook 01: `01_load_data.ipynb`

**Purpose:** pipeline sanity and dataset trust check.

Run this first to verify:

- dataset path is correct.
- expected files exist.
- point clouds load correctly.
- labels load correctly.
- point-label alignment is valid.
- basic intensity and range statistics look reasonable.

## Notebook 02: `02_single_frame_reflectivity_analysis.ipynb`
**Purpose:** single-frame reflectivity-style analysis.

Run this next to:

- inspect one frame in detail.
- compute range and pseudo-reflectivity.
- compare raw intensity vs $I \cdot R$.
- quantify range dependence.
- quantify semantic separability on one frame.
- build first bird's-eye and FOV reflectivity-style visualizations.

## Notebook 03: `03_multi_frame_reflectivity_over_motion.ipynb`
**Purpose:** short-window motion analysis.

Run this to:

- load a 30-frame contiguous motion window.
- compute frame-wise summaries of intensity, range, and pseudo-reflectivity.
- inspect temporal stability.
- check whether the signal remains structured over motion.
- generate a 30-frame comparison GIF.

## Notebook 04: `04_single_frame_semantic_reflectivity_analysis.ipynb`
**Purpose:** attach signal behavior directly to semantics.

Run this to:

- inspect semantic classes in one labeled frame.
- compute class-wise signal statistics.
- compare raw intensity vs pseudo-reflectivity distributions per class.
- compute multiclass separability.
- generate semantic visualizations in BEV / FOV style.

## Notebook 05: `05_multi_frame_semantic_consistency.ipynb`
**Purpose:** test whether Notebook 04’s class-wise patterns survive motion.

Run this to:

- compute class-wise statistics over a short multi-frame window.
- keep only temporally persistent classes.
- measure class-ordering consistency across frames.
- quantify whether pseudo-reflectivity preserves semantic class structure through motion.
- generate a labeled reflectivity-augmented semantic GIF.

# Mathematical workflow used in the preliminary notebooks

For each frame:

## Load points
SemanticKITTI point cloud files are read as float32 and reshaped to `N x 4`:

```python
points = np.fromfile(bin_path, dtype=np.float32).reshape(-1, 4)
xyz = points[:, :3]
intensity = points[:, 3]
```

## Load labels
Semantic labels are unpacked from the lower 16 bits:

```python
raw = np.fromfile(label_path, dtype=np.uint32)
semantic_labels = raw & 0xFFFF
```

## Compute range

```python
ranges = np.linalg.norm(xyz, axis=1)
```

## Compute pseudo-reflectivity

```python
pseudo_reflectivity = intensity * ranges
```

## Compute class separability
A Fisher-style multiclass separability score is used in the preliminary analysis:

$$
\text{score} = \frac{\text{between-class dispersion}}{\text{within-class dispersion}}
$$

Higher values indicate stronger class separation.

## Measure temporal class consistency
For Notebook 05, class-wise mean profiles across frames are compared using **Spearman rank correlation**. This checks whether the ordering of classes remains stable through motion.

# Result discussion

![bev_forward_intensity_vs_pr_30f](assets/notebook03_bev_forward_intensity_vs_pr_30f.gif)

![reflectivity_augmented_semantic_motion_30f_labeled](assets/notebook05_reflectivity_augmented_semantic_motion_30f_labeled.gif)

## What clearly worked

### A. Pipeline correctness
The project successfully loaded SemanticKITTI point clouds and labels, verified alignment, and built reproducible notebook logic around that structure.

### B. Range-aware augmentation is actually doing something nontrivial
The proxy $I \cdot R$ is not identical in behavior to raw intensity. It changes distributions, class ordering, and spatial emphasis in a measurable way.

### C. Single-frame semantic discrimination improved
On the inspected frame, the proxy improved class separability clearly. That is one of the strongest preliminary findings.

### D. Temporal stability exists
The signal does not collapse the moment motion enters the room. Over short windows, it stays smooth, structured, and visually interpretable.

### E. Semantic class structure persists across motion
The class-wise story is not a one-frame hallucination. Short-window consistency analysis suggests that the semantic ordering is highly stable.

## What did **not** get solved

### A. This is not true reflectivity recovery
The proxy is still range-dependent. It is not calibrated reflectance, and it cannot be presented as such.

### B. Material identification is not solved yet
At this stage, brightness modulation within semantic structure is being studied. The project is not yet detecting or confidently inferring material categories.

### C. Global dominance was not shown
Pseudo-reflectivity is not better than raw intensity in every frame or every scene regime. The motion analysis showed flips in advantage.

### D. The current evaluation is still exploratory
The preliminary stage is built around descriptive statistics, separability metrics, rank consistency, and visualization. That is appropriate for feasibility, but not yet enough for a big final claim.

# Current preliminary conclusion

A clean and honest preliminary conclusion is:

> Initial experiments on SemanticKITTI indicate that a simple range-aware pseudo-reflectivity proxy $(I \cdot R)$ produces a modest but consistent improvement in semantic discriminability relative to raw intensity alone. This effect is visible in single-frame signal statistics, short-window motion analysis, and class-wise semantic inspection. The proxy remains range-dependent and scene-dependent, so it should not be interpreted as true calibrated reflectivity. However, it appears stable and informative enough to justify a broader final-stage study.

That is the correct preliminary claim. Clean, sharp, and still wearing a seatbelt.

# Generated artifacts in the preliminary stage

Depending on which notebooks are executed, the preliminary work can produce:

- dataset sanity outputs and structural verification logs
- BEV and FOV single-frame visualizations
- class-wise summary tables
- temporal plots across selected frame windows
- a 30-frame BEV/FOV comparison GIF
- a labeled reflectivity-augmented semantic motion GIF

These outputs are meant to support the preliminary report and to make the idea defensible with both numbers and visuals.

# What should be expanded in the final stage

The final phase should go beyond notebook exploration and build the heavier contribution.

## 1. Broader multi-frame / sequence-level evaluation
Expand beyond a small temporal window.

Possible final work:

- analyze many more frames
- aggregate results over longer time horizons
- compute mean, variance, and trend behavior over larger sequence chunks

## 2. Proxy comparison
Right now the preliminary stage uses \(I \cdot R\). The final stage should compare lightweight alternatives such as:

- $I \cdot R$.
- $I \cdot R^2$.
- $\log(1 + I \cdot R)$.
- normalized or clipped variants.
- robust-scaled versions.

## 3. Stronger metrics
Add more mature final-stage metrics such as:

- per-class separability change.
- temporal variance of class statistics.
- intra-class compactness vs inter-class distance.
- frame-wise distributions of improvement.
- broader rank-consistency analysis.

## 4. Failure-case analysis
A real final project should not only show wins. It should also inspect where things break.

Possible failure-mode analysis:

- classes helped strongly.
- classes helped weakly.
- classes hurt by the proxy.
- far-range sparsity effects.
- class imbalance effects.
- scene geometry dependence.

## 5. Lightweight downstream usefulness study

A valuable final addition would be checking whether pseudo-reflectivity helps a simple downstream semantic task.

Examples:

- intensity-only vs intensity-plus-proxy feature comparison.
- lightweight classifier on selected classes.
- toy semantic ablation study.

This would move the project from “looks helpful” to “is helpful”.

## 6. Engineering / modular packaging
The final stage should turn the current notebook work into a cleaner reusable code structure.

Possible final deliverable:

- modular preprocessing component.
- input: point cloud + intensity.
- output: augmented point cloud + pseudo-reflectivity.
- optional ROS2-style preprocessing node.

That would make the project more robotics-real and less notebook-only.

# What remains the honest framing for the final project

Even in the final phase, the safe claim is still:

- reflectivity-aware scene analysis.
- semantic interpretation through motion.
- reflectivity-aware temporal scene understanding.

# Reproducibility notes

- Run notebooks from the `notebooks/` directory so relative paths resolve correctly.
- Keep dataset files out of git if the repository is public or lightweight.
- Use fixed visualization ranges for GIF creation so the motion visuals do not become misleading through autoscaling.
- Execute notebooks in order because the interpretation ladder is intentionally staged.

# One-line summary

**Preliminary:** prove that reflectivity-aware LiDAR analysis works on one frame and a short motion window, with a disciplined semantic glimpse.

**Final (Tentative):** scale that into a stronger multi-frame semantic scene-understanding pipeline with broader evaluation, better metrics, proxy comparison, failure analysis, and modular engineering structure.

---