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

## Inspiration from Prior Research

This project was directly inspired by the paper **“Reflectivity Is All You Need!: Advancing LiDAR Semantic Segmentation”** by Viswanath, Jiang, and Saripalli (https://arxiv.org/abs/2403.13188). A key idea I took from that work is that raw LiDAR intensity is not a clean surface descriptor by itself, because it is affected by measurement geometry, especially **range** and **incidence angle**, whereas calibrated reflectivity can provide a more consistent and interpretable signal for scene understanding.

The main lesson I carried into this preliminary project was not to claim full reflectivity recovery too early, but to treat reflectivity-style reasoning as a **practical signal-analysis problem**. Since full calibration terms were outside the scope of this stage, I adopted a deliberately lightweight and honest approximation: a **range-aware pseudo-reflectivity proxy**, using $\hat{\rho} = I \cdot R$, to test whether a simple correction of raw intensity could reveal scene structure more clearly than intensity alone.

So, rather than attempting material identification or a full semantic segmentation model in the preliminary phase, this work focuses on a narrower question: **can a simple range-aware augmentation of raw LiDAR intensity make the signal more interpretable for robotic scene understanding?** That idea shaped the design of the current notebooks and will continue into the final stage, where I plan to evaluate the same reflectivity-aware intuition more broadly across time, classes, and stronger downstream analyses. 

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
├── LICENSE                            # MIT LICENSE
│
├── notebooks/                         # Preliminary Work
│   ├── artifacts/                     # GIF Plots
│   ├── notebooks_pdf/                 # Author's Implementation
│   ├── 01_load_data.ipynb
│   ├── 02_single_frame_reflectivity_analysis.ipynb
│   ├── 03_multi_frame_reflectivity_over_motion.ipynb
│   ├── 04_single_frame_semantic_reflectivity_analysis.ipynb
│   ├── 05_multi_frame_semantic_consistency.ipynb
│   ├── mid-term-project-report.pdf    # Submission Artifact
│   └── README.md                      # This File (Prelim README)
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
├── results/                            # For Final Work
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
**Purpose:** test whether Notebook 04’s class-wise patterns survive motion over a short preliminary window.

Run this to:

- compute class-wise statistics over a 10-frame multi-frame window used for the semantic consistency analysis.
- keep only temporally persistent classes.
- measure class-ordering consistency across frames.
- quantify whether pseudo-reflectivity preserves semantic class structure through motion.
- generate a labeled reflectivity-augmented semantic GIF over a separate 30-frame visualization window.

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

# Result Discussion (Preliminary)

**Note**: For author's execution, have a look at all the pdf files in `notebooks_pdf` folder.

![bev_forward_intensity_vs_pr_30f](artifacts/notebook03_bev_forward_intensity_vs_pr_30f.gif)

![reflectivity_augmented_semantic_motion_30f_labeled](artifacts/notebook05_reflectivity_augmented_semantic_motion_30f_labeled.gif)

## What clearly worked

### A. Pipeline correctness
The project successfully loaded SemanticKITTI point clouds and labels, verified alignment, and built reproducible notebook logic around that structure.

### B. Range-aware augmentation is actually doing something nontrivial
The proxy $I \cdot R$ is not identical in behavior to raw intensity. It changes distributions, class ordering, and spatial emphasis in a measurable way.

### C. Single-frame semantic discrimination improved
On the inspected semantic frame, the proxy improved multiclass separability modestly but clearly. In Notebook 04, the Fisher-style score increased from 0.448162 for raw intensity to 0.505541 for pseudo-reflectivity, corresponding to an absolute improvement of 0.057379 and a relative improvement of about 12.8%.

### D. Temporal stability exists
The signal does not collapse the moment motion enters the room. In Notebook 03, over a 30-frame motion window, pseudo-reflectivity remained numerically stable and visually structured, while still retaining clear range dependence. In particular, the mean correlation between raw intensity and range was -0.206539, whereas the mean correlation between pseudo-reflectivity and range was 0.364621.

### E. Semantic class structure persists across motion
The class-wise story is not a one-frame hallucination. In Notebook 05, over a 10-frame semantic consistency window, class ordering remained highly stable for both raw intensity and pseudo-reflectivity. The mean Spearman rank correlation versus the average class profile was 0.9534 for raw intensity and 0.9582 for pseudo-reflectivity, indicating a mild short-window consistency advantage for the proxy rather than a dramatic dominance claim.

## What did **not** get solved

### A. This is not true reflectivity recovery
The proxy is still range-dependent. It is not calibrated reflectance, and it cannot be presented as such.

### B. Material identification is not solved yet
At this stage, brightness modulation within semantic structure is being studied. The project is not yet detecting or confidently inferring material categories.

### C. Global dominance was not shown
Pseudo-reflectivity is not better than raw intensity in every frame or every scene regime. Notebook 03 showed that its semantic advantage is motion- and scene-dependent rather than uniform: it is stronger in the early part of the 30-frame window, weaker in the middle where raw intensity temporarily becomes more separable, and then positive again later with a milder advantage.

### D. The current evaluation is still exploratory
The preliminary stage is built around descriptive statistics, separability metrics, rank consistency, and visualization. That is appropriate for feasibility, but not yet enough for a big final claim.

# Current preliminary conclusion

A clean and honest preliminary conclusion is:

> Initial experiments on SemanticKITTI indicate that a simple range-aware pseudo-reflectivity proxy $(I \cdot R)$ can produce a **modest overall improvement** in semantic discriminability relative to raw intensity alone, but this benefit is **not uniform** across motion or scene composition. The effect is visible in single-frame analysis, short-window motion analysis, and class-wise semantic inspection. The proxy remains range-dependent and scene-dependent, so it should not be interpreted as true calibrated reflectivity. However, it appears stable and informative enough to justify a broader final-stage study.

# Generated artifacts in the preliminary stage

Depending on which notebooks are executed, the preliminary work can produce:

- dataset sanity outputs and structural verification logs.
- BEV and FOV single-frame visualizations.
- class-wise summary tables.
- temporal plots across selected frame windows.
- a 30-frame BEV/FOV comparison GIF.
- a labeled reflectivity-augmented semantic motion GIF over 30 frames, separate from the 10-frame class-consistency analysis window used in Notebook 05.

# What should be expanded in the final work

The preliminary work established that a lightweight range-aware pseudo-reflectivity proxy can produce structured, semantically meaningful behavior on single frames and across short motion windows. The final stage should now move beyond feasibility-style notebook analysis and turn this into a broader, more rigorous, and more robotics-relevant study.

## 1. Broader temporal and sequence-level evaluation

The preliminary phase intentionally used small motion windows to remain disciplined. The final stage should expand this into a more representative temporal study.

Possible extensions include:

- analyzing substantially longer frame windows instead of only short preliminary segments,
- evaluating multiple parts of the sequence rather than a single local region,
- aggregating signal behavior over longer horizons,
- measuring how stable the conclusions remain across different scene compositions.

This matters because a useful perception cue should not only work in one short window, but remain interpretable across broader motion and changing environmental structure.

## 2. Proxy comparison and alternative formulations

The preliminary phase focused on the simple proxy

$$
\hat{\rho} = I \cdot R
$$

because it is lightweight, easy to compute, and sufficient for feasibility testing. The final stage should test whether this is actually the best practical formulation among other simple range-aware transformations.

Possible proxy variants include:

- $I \cdot R$,
- $I \cdot R^2$,
- $\log(1 + I \cdot R)$,
- clipped or percentile-normalized variants,
- robust-scaled versions,
- per-frame or per-sequence normalized forms.

This comparison is important because the current proxy was chosen as a disciplined first probe, not as a guaranteed optimum.

## 3. Stronger and more targeted metrics

The preliminary evaluation relied on descriptive statistics, Fisher-style separability, temporal trend inspection, and rank-consistency analysis. The final stage should strengthen this with a broader and more diagnostic metric set.

Useful final-stage metrics could include:

- per-class separability change,
- temporal variance of class-wise statistics,
- intra-class compactness versus inter-class distance,
- frame-wise gain distributions showing where the proxy helps and where it hurts,
- rank-consistency analysis across longer windows and more scene regimes,
- summary statistics over multiple windows rather than single-window snapshots.

This would make the conclusions less notebook-local and more quantitatively grounded.

## 4. Failure-case and limitation analysis

A serious final project should not only emphasize the frames where the proxy looks strong. It should also identify the conditions under which the benefit weakens or reverses.

Possible failure-case analysis includes:

- classes that are helped strongly,
- classes that are helped only marginally,
- classes that are hurt by the proxy,
- far-range sparsity effects,
- class imbalance effects,
- dependence on local scene geometry,
- motion windows where raw intensity temporarily becomes more useful than the proxy.

This is especially important because the preliminary work already showed that the advantage of pseudo-reflectivity is scene-dependent rather than uniform.

## 5. Surface-sensitive and material-like interpretation

The preliminary phase did **not** attempt material identification, and it should not be presented as doing so. However, one natural final-stage extension is to investigate whether reflectivity-aware cues can support more refined surface interpretation within and across semantic classes.

Possible directions include:

- studying within-class surface variation, such as differences inside road, building, vegetation, or terrain regions,
- checking whether reflectivity-aware features expose material-like structure more clearly than raw intensity,
- identifying whether some semantic classes consistently split into more interpretable subgroups under the proxy,
- testing whether the proxy supports surface-property-sensitive analysis without claiming full material recovery.

This would be a strong extension because it builds directly on the current results while staying scientifically honest.

## 6. Lightweight downstream usefulness study

A valuable final-stage question is whether pseudo-reflectivity is useful not only for analysis, but also as an additional feature in a simple downstream semantic task.

Possible studies include:

- comparing intensity-only features against intensity-plus-proxy features,
- training a lightweight classifier on selected semantic classes,
- performing a small semantic ablation study,
- testing whether the proxy improves separability or classification on carefully chosen subsets.

This would help move the project from “interesting signal analysis” toward “useful perception feature.”

## 7. Engineering and modular packaging

The final stage should also reduce dependence on notebooks by turning the current workflow into a cleaner reusable code structure.

Possible engineering deliverables include:

- a modular preprocessing component,
- a reusable loader for LiDAR frames and labels,
- a feature-generation module for pseudo-reflectivity and related variants,
- a temporal analysis module for multi-frame evaluation,
- visualization utilities for BEV and forward-view comparisons.

A clean final pipeline could have the following logic:

- **input:** point cloud + raw intensity,
- **processing:** range computation + reflectivity-aware feature generation,
- **output:** augmented point cloud with pseudo-reflectivity and analysis-ready summaries.

This would make the project more reproducible, more maintainable, and more robotics-real rather than notebook-only.

## Final-stage objective in one line

The final stage should transform the current preliminary evidence into a broader reflectivity-aware LiDAR scene-understanding study that is temporally stronger, metrically sharper, failure-aware, and more useful for downstream robotic perception.

# Reproducibility notes

- Run notebooks from the `notebooks/` directory so relative paths resolve correctly.
- Keep dataset files out of git if the repository is public or lightweight.
- Use fixed visualization ranges for GIF creation so the motion visuals do not become misleading through autoscaling.
- Execute notebooks in order because the interpretation ladder is intentionally staged.

# Academic Context & Acknowledgment

This preliminary project was completed as part of **SES 598: Space Robotics & AI** at Arizona State University, under the guidance of **Prof. Jnaneshwar Das**.

The course is affiliated with the **Distributed Robotic Exploration and Mapping Systems (DREAMS) Laboratory**

- **DREAMS Lab GitHub:** https://github.com/DREAMS-lab  
- **DREAMS Lab:** https://deepsig.org/dreamslab  

The overall project framing, evaluation discipline, and robotics context were shaped by the course environment and by broader research themes in robotic perception, exploration, and autonomous systems associated with the course and DREAMS lab.

This work represents the author’s independent preliminary implementation and analysis carried out within that academic setting.

---