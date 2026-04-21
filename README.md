# 📡 **Reflect-Aug-Seg** 🔦🫧

## Reflectivity-Augmented LiDAR Scene Understanding for Robotic Perception

> **Author:** Ayushman Mishra  
> **Course:** SES 598: Space Robotics & A.I.  
> **Institution:** Arizona State University

---

## Abstract

**Reflect-Aug-Seg** studies whether a lightweight, range-aware transformation of LiDAR intensity can provide a more useful semantic cue than raw intensity alone for robotic perception.

The central motivation is simple: raw LiDAR intensity is **not** a clean intrinsic surface property. It is entangled with range, incidence geometry, and sensor behavior. So instead of pretending that raw intensity is already reflectivity, this project introduces and evaluates a practical pseudo-reflectivity proxy:

`rho_hat = I * R`

where `I` is raw **LiDAR intensity** and `R` is **point-wise Euclidean range**.

This project is not a calibrated reflectivity-recovery system, and it does not claim material identification or state-of-the-art semantic segmentation performance. Instead, it asks a more disciplined question:

> Can a physically motivated, range-aware signal augmentation improve semantic interpretability and lightweight downstream usefulness in LiDAR scene understanding?

The work starts from a midterm feasibility study on **SemanticKITTI** and is extended into a broader final pipeline that adds:

- a compact baseline lock of the preliminary work,
- structured **multi-window evaluation** across sequence 00,
- comparison of multiple proxy variants,
- stronger signal and semantic diagnostics,
- explicit failure-case analysis,
- modular artifact generation using `src/` + `scripts/`, and
- a lightweight downstream classification study.

The final project demonstrates that reflectivity-aware augmentation is a meaningful and measurable signal transformation rather than a trivial rescaling of intensity. The direct proxy I · R consistently alters signal structure and yields clear semantic gains in multiple frames and windows, while also exposing its dependence on scene composition and range distribution.

Across multi-window analysis, a stabilized variant, log(1 + I · R), shows more consistent behavior and improved robustness as an analysis-side signal. At the same time, the direct proxy remains practically useful: it improves a lightweight downstream classifier and produces interpretable BEV and FOV visualizations that preserve semantic structure over motion.

Overall, the project establishes reflectivity-aware features as a lightweight, computation-free augmentation that can enhance LiDAR signal interpretability, while clearly identifying the conditions under which their benefits are strongest.

That balance is the central result:

- measurable semantic improvement is consistently observed,
- the magnitude of that improvement varies with scene structure and range distribution,
- and these conditions are explicitly characterized rather than treated as noise.

This positions reflectivity-aware augmentation as a controlled, interpretable signal enhancement, not a universally dominant feature.

---

## Project Idea in One Paragraph

LiDAR provides reliable geometry, but its intensity channel is entangled with range and measurement geometry, making it an unreliable proxy for surface properties. This work investigates whether a simple range-aware transformation, I · R, can produce a more semantically informative signal. The approach is deliberately lightweight: instead of attempting full reflectivity calibration or learning an inverse model, it introduces a controlled proxy that can be analyzed quantitatively, semantically, temporally, and visually.

### Inspiration from Prior Work

This work is partially inspired by *“Reflectivity Is All You Need!”* by Kasi Viswanath, Peng Jiang, and S. Saripalli, which explores the use of calibrated reflectivity as a more informative signal for LiDAR-based semantic understanding.

That paper demonstrates that incorporating reflectivity into learning-based models can improve segmentation performance by providing a more consistent representation than raw intensity.

This work draws inspiration from that central idea, that reflectivity-related information can enhance LiDAR perception. However, instead of pursuing calibrated reflectivity recovery or integrating it into deep learning pipelines, this work investigates a simpler question: whether a lightweight, range-aware transformation of intensity can reveal similar semantic structure.

The connection is therefore conceptual rather than methodological, focusing on extracting signal-level insights rather than reproducing a full reflectivity estimation pipeline.

## Why This Work Matters

This work addresses a practical gap between raw intensity usage and full reflectivity modeling.

It introduces a lightweight, range-aware signal transformation that:

- improves semantic separability in a measurable way,
- remains computationally simple and easy to integrate,
- and enables structured analysis of signal behavior across time and scenes.

Rather than aiming for full physical recovery, the focus is on **interpretable and controlled signal enhancement**, making the approach suitable for real-time robotic perception systems where simplicity, stability, and clarity of behavior are critical.

---

## Mathematical Modeling

Each LiDAR point is represented as:

`p_i = (x_i, y_i, z_i, I_i)`

where:

- `(x_i, y_i, z_i)` are Cartesian coordinates,
- `I_i` is the recorded raw intensity.

The Euclidean range is:

`R_i = sqrt(x_i^2 + y_i^2 + z_i^2)`

A simplified return-strength model is:

`I_i ∝ (rho_i * cos(alpha_i)) / R_i^2`

where:

- `rho_i` is surface reflectivity,
- `alpha_i` is incidence angle,
- `R_i` is range.

This immediately tells us that raw intensity mixes together:

- intrinsic surface behavior,
- distance effects,
- geometric incidence effects,
- and sensor-specific response.

So this work does **not** equate raw intensity with reflectivity.

Instead, it defines a practical pseudo-reflectivity proxy:

`rho_hat_i = I_i * R_i`

This proxy is:

- computationally trivial,
- easy to deploy,
- physically motivated,
- and effective for signal analysis,

while remaining a lightweight, range-aware approximation rather than a fully calibrated reflectivity estimate.

### Important Clarification

The proxy ρ̂ = I · R is not a calibrated reflectivity estimate.

It is a deliberately simplified, range-aware transformation designed to reshape the raw intensity signal for improved semantic interpretability, without attempting full physical reflectance recovery.

---

## Scope and Boundaries

This work is intentionally scoped as a reflectivity-aware signal analysis study, not a full reflectivity reconstruction, material identification, or semantic segmentation system.

The focus is on:

- analyzing how range-aware transformations reshape LiDAR intensity,
- quantifying their semantic impact across frames and motion,
- and identifying the conditions under which these transformations improve or degrade signal structure.

This scope is deliberate. LiDAR intensity is inherently entangled with range and measurement geometry (e.g., incidence angle), making direct recovery of surface reflectivity or material properties an underdetermined problem without additional calibration or sensing modalities.

Accordingly, this work does not attempt calibrated reflectivity recovery, material identification, or benchmark-driven segmentation performance claims. It also does not treat visually smooth outputs as evidence of physical correctness.

Instead, the work concentrates on controlled, interpretable signal transformations that are lightweight, reproducible, and analytically grounded, while explicitly characterizing their strengths and limitations across different scene conditions.

---

## From Midterm to End: What Changed and What Improved

The midterm stage established feasibility using **SemanticKITTI sequence 00** and a staged notebook workflow. It demonstrated that a simple range-aware proxy, I · R, can alter LiDAR signal structure and produce measurable semantic gains.

### Midterm baseline (what was established)

- Single-frame semantic separability improved from **0.4482** (raw intensity) to **0.5055** (pseudo-reflectivity)  
  - Absolute gain: **+0.0574**  
  - Relative gain: **+12.8%**
- Across a short 10-frame window, class-ordering stability remained high:
  - **0.9534** (raw intensity)  
  - **0.9582** (pseudo-reflectivity)

These results confirmed that the idea was valid, but limited in scope: evaluation was local, proxy design was fixed, and scene-dependent behavior was not yet characterized.

### Final work (what was improved and added)

The final stage preserves the midterm baseline and extends it into a broader, more rigorous study.

#### 1. From single-window → multi-window evaluation

- Midterm: analysis restricted to short, local frame segments.  
- Final: evaluation extended across multiple temporal windows.  

**Result:** improved reliability and reduced dependence on hand-picked examples.

#### 2. From single proxy → proxy family analysis

- Midterm: focused on `I · R`.  
- Final: evaluated multiple variants (e.g., `log(1 + I · R)`).
  
→ **Result:** identified more stable and robust transformations for analysis.

#### 3. From local behavior → global signal characterization

- Midterm: observations limited to individual frames or short motion.  
- Final: signal statistics and trends analyzed across windows.  

→ **Result:** clearer understanding of temporal stability and range dependence.

#### 4. From single-frame semantics → multi-window semantic trends

- Midterm: separability evaluated on isolated frames and short windows.  
- Final: semantic gains tracked across time and scene variation.  

→ **Result:** quantified where improvements persist and where they degrade.

#### 5. From implicit bias → explicit failure-case analysis

- Midterm: weak cases were visible but not systematically studied.  
- Final: best and worst frames identified and analyzed.  

→ **Result:** grounded understanding of scene-dependent performance.

#### 6. From analysis-only → lightweight downstream validation

- Midterm: signal usefulness demonstrated analytically.  
- Final: tested via a simple classifier.
  
→ **Result:** confirmed that improvements translate to feature-level utility.

#### 7. From notebooks → modular pipeline

- Midterm: exploratory notebooks.  
- Final: structured pipeline (`src/`, `scripts/`, reproducible runs).  

→ **Result:** improved reproducibility and engineering quality.

### Overall progression

The midterm established that reflectivity-aware augmentation is feasible and semantically meaningful at a local level.

The final work extends this into a **multi-window, failure-aware, and quantitatively grounded analysis**, showing that:

- improvements are **real and measurable**,  
- their magnitude is **scene- and context-dependent**,  
- and their behavior can be **systematically characterized rather than observed anecdotally**.

---

## Final Repository Structure

Below is the current repository structure as provided:

```text
.
├── artifacts               # Create if does not exist.
│   ├── final_seq.csv
│   └── final_seq.gif
├── data                    # Download through SemanticKITTI website.
│   └── semantickitti
│       └── dataset
│           └── sequences
│               ├── 00
│               ├── 01
│               ├── 02
│               │   .
│               │   .
│               └── 21
├── final_pipeline_stepwise
│   ├── 01_preliminary_work_recap.pdf
│   ├── 02_multiwindow_sequence_setup.pdf
│   ├── 03_proxy_variant_builder.pdf
│   ├── 04_multiwindow_global_signal_analysis.pdf
│   ├── 05_multiwindow_semantic_analysis.pdf
│   ├── 06_failure_case_analysis.pdf
│   ├── 07_video_gif_asset_builder.pdf
│   ├── 08_lightweight_downstream_study.pdf
│   └── full-reflect-aug-seg-pipeline.pdf
├── LICENSE
├── notebooks_midterm_w     # Midterm Work
│   ├── 01_load_data.pdf
│   ├── 02_single_frame_reflectivity_analysis.pdf
│   ├── 03_multi_frame_reflectivity_over_motion.pdf
│   ├── 04_single_frame_semantic_reflectivity_analysis.pdf
│   ├── 05_multi_frame_semantic_consistency.pdf
│   └── mid-term-project-report.pdf
├── README.md
├── requirements.txt
├── scripts
│   ├── generate_gif.py
│   └── run_command_60_sec.txt
└── src
    ├── animation
    │   └── gif_writer.py
    ├── io
    │   ├── loader.py
    │   └── sequence_sampler.py
    ├── metrics
    │   ├── csv_logger.py
    │   └── separability.py
    ├── semantics
    │   ├── class_stats.py
    │   └── label_map.py
    ├── signals
    │   └── reflectivity.py
    └── visualization
        └── frame_renderer.py
```

### Folder meanings

#### `notebooks_midterm_w/`
Frozen archive of the preliminary/midterm work. This is the original feasibility staircase.

#### `final_pipeline_stepwise/`
The final narrative, organized notebook-by-notebook as exported PDFs.

#### `src/`
Reusable modular implementation for data loading, signal construction, semantic handling, metrics, visualization, and GIF writing.

#### `scripts/`
Entry-point scripts for artifact generation and reproducible execution.

#### `artifacts/`
Final generated outputs, including the provided 60-second GIF and its matching CSV log.

---

## Dataset

This work uses the **SemanticKITTI** dataset, a large-scale semantic LiDAR dataset built on the KITTI Odometry Benchmark.

### Official dataset source

- SemanticKITTI official site: <https://semantic-kitti.org/>
- SemanticKITTI API repository: <https://github.com/PRBonn/semantic-kitti-api>


### Dataset size note

The full SemanticKITTI dataset is **large (~80 GB)**. 

Users with limited bandwidth or storage constraints are advised to:

- download only the required sequences (e.g., 00–02 for quick experiments),
- or work with a subset of the dataset for initial testing.

### Expected dataset placement

The code expects the dataset in this form:

```text
data/
└── semantickitti/
    └── dataset/
        └── sequences/
            ├── 00/
            │   ├── calib.txt
            │   ├── poses.txt
            │   ├── times.txt
            │   ├── velodyne/
            │   │   ├── 000000.bin
            │   │   ├── 000001.bin
            │   │   └── ...
            │   └── labels/
            │       ├── 000000.label
            │       ├── 000001.label
            │       └── ...
            ├── 01/
            ├── 02/
            └── ...
```

- The **midterm stage** was centered on **SemanticKITTI sequence 00** for controlled feasibility validation.

- In the **final pipeline**, sequences are **not fixed**. Instead, a contiguous frame window is **randomly sampled from a set of allowed sequences** (default: 00–21), enabling broader temporal and scene diversity.

- The provided `final_seq.csv` and `final_seq.gif` artifacts correspond to **one such sampled run**, and therefore reflect pipeline behavior on a **randomly selected sequence window**, not a fixed sequence.

- This sampling behavior is controlled via the execution command, where multiple sequences are explicitly allowed:

  ```bash
  --sequences 00 01 02 ... 21
  ```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/aymisxx/reflect-aug-seg
cd reflect-aug-seg
```

### 2. Create a Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Place the dataset

Download SemanticKITTI from the official source and place the folders under:

```bash
data/semantickitti/dataset/sequences/
```

Make sure the sequence folders contain both:

- `velodyne/*.bin`
- `labels/*.label`

along with `calib.txt`, `poses.txt`, and `times.txt`.

---

## **How the Work Was Done (The Pipeline)**

The full final pipeline is documented in `final_pipeline_stepwise/` and proceeds in eight stages.

## Stage 01: Preliminary Work Recap / Baseline Lock

Purpose:

> Rebuild the midterm logic in one compact final-stage notebook.

> Verify that the data pipeline, labels, basic signal behavior, and semantic recap still hold.

This stage re-establishes:

- dataset integrity,
- point-label alignment,
- raw intensity behavior,
- pseudo-reflectivity behavior,
- short-window motion stability,
- single-frame semantic effect,
- and short-window semantic consistency.

This is the “baseline lock.”

## Stage 02: Multi-Window Sequence Setup

Purpose:

> Convert sequence 00 into a structured, reproducible temporal evaluation framework.

The final work defines **15 windows** across sequence 00:

### Short windows (length 10)

- `short_0`: 000000–000009
- `short_1`: 001132–001141
- `short_2`: 002265–002274
- `short_3`: 003398–003407
- `short_4`: 004531–004540

### Medium windows (length 30)

- `medium_0`: 000000–000029
- `medium_1`: 001127–001156
- `medium_2`: 002255–002284
- `medium_3`: 003383–003412
- `medium_4`: 004511–004540

### Long windows (length 100)

- `long_0`: 000000–000099
- `long_1`: 001110–001209
- `long_2`: 002220–002319
- `long_3`: 003330–003429
- `long_4`: 004441–004540

This was a major methodological improvement over the midterm, because it removed dependence on one hand-picked local segment.

## Stage 03: Proxy Variant Builder

Purpose:

> Test whether `I * R` is the best practical proxy, or only the first useful one.

### Proxy family explored

- Raw intensity: `I`.
- Direct range-aware proxy: `I * R`.
- Aggressive proxy: `I * R^2`.
- Log-scaled proxy: `log(1 + I * R)`.
- Percentile-normalized proxy.
- Robust-scaled proxy.

### Main outcome

- `I * R^2` was rejected because it caused severe distribution explosion and strong range domination.
- `I * R` remained meaningful and interpretable.
- `log(1 + I * R)` emerged as the best-balanced analysis-side proxy for stability and controlled range behavior.

## Stage 04: Multi-Window Global Signal Analysis

Purpose:

> Evaluate whether proxies behave consistently across different temporal segments.

This stage measured, per window:

- mean,
- standard deviation,
- percentiles,
- and correlation with range.

### Main quantitative stability summary

| Proxy | Mean of means | Std of means | Variance of means | CV |
|---|---:|---:|---:|---:|
| `I` | 0.293709 | 0.011757 | 0.000138 | 0.040029 |
| `I * R` | 3.376979 | 0.216696 | 0.046957 | 0.064169 |
| `log(1 + I*R)` | 1.279784 | 0.049860 | 0.002486 | 0.038960 |

### Interpretation

- Raw intensity is stable, but limited.
- `I * R` is expressive, but more variable.
- `log(1 + I * R)` achieved the best balance between stability and useful range-aware restructuring.

## Stage 05: Multi-Window Semantic Analysis

Purpose:

> Determine whether proxy signals improve semantic structure **across many windows**, not just one frame.

Semantic usefulness was evaluated with a Fisher-style multiclass separability score:

`S = between-class variance / within-class variance`

Per-window gain was then defined as:

`delta_S = S_proxy - S_raw`

### Main conclusion

- The direct proxy `I * R` was **highly variable**.
- It produced strong gains in some windows, but negative dips in others.
- The log-scaled proxy `log(1 + I * R)` was much more robust and consistently positive.

This was the strongest final-stage evidence that **proxy design matters**, not just the initial reflectivity idea.

## Stage 06: Failure Case Analysis

Purpose:

> Explain where the method weakens and why.

Using the multi-window separability results, windows were classified into:

- failure cases,
- weak-performance cases,
- strong cases.

### Log-scaled proxy outcome

Across the 15 windows:

- **Failures:** 0.
- **Weak cases:** 1 (`short_3`).
- **Strong cases:** 14.

### Strong vs weak representative windows

- Weak case: `short_3`
- Strong case: `short_2`

### Failure mechanism

The analysis showed that weak performance was not caused by missing data or numerical collapse. Instead, it came from **class-wise signal overlap**:

- in strong windows, class means were spread apart,
- in weak windows, class means were compressed,
- reduced spacing led to higher overlap and lower separability.

This result captures both the strengths and the limitations of the approach, providing a clearer understanding of when and how the method is effective.

## Stage 07: Video / GIF Artifact Builder

Purpose:

> Turn the analytical work into controlled visual artifacts.

### What was built

- BEV visualization.
- Forward/FOV visualization.
- signal comparison boards.
- semantic overlays.
- legend + top-class summary panel.
- temporal frame renderer.
- GIF-based artifact generation.

### Rendering discipline

Artifacts were built under strict constraints:

- fixed spatial limits,
- fixed normalization across frames,
- deterministic subsampling,
- no per-frame visual manipulation.

That matters because many visualizations look “better” only because they cheat by rescaling every frame independently. This work avoids that.

## Stage 08: Lightweight Downstream Study

Purpose:

> Test whether the proxy gives practical feature-level value in a simple classification setup.

### Dataset used

A single medium window (`medium_0`) was used.

- Frames: 30
- Total points: 3,697,281
- After filtering: 3,621,402
- Valid classes: `[1, 10, 40, 44, 48, 50, 51, 52, 60, 70, 71, 72, 80, 81, 99]`

### Feature sets

- Baseline: `[I]`
- Augmented: `[I, I * R]`

### Training setup

- Random subsample: **200,000** points.
- Train/test split: **80/20**.
- Baseline feature shape: `(3621402, 1)` before subsampling.
- Augmented feature shape: `(3621402, 2)` before subsampling.
- Model: **Logistic Regression**.
- Features scaled with `StandardScaler`.

### Downstream result

| Configuration | Accuracy |
|---|---:|
| `I` only | 0.377925 |
| `I + I*R` | 0.409025 |
| Absolute gain | **+0.031100** |

### Interpretation

The observed **+3.11 percentage-point** improvement comes from a deliberately simple setup, yet it captures a much stronger underlying effect.

The gains are **not uniform across classes**, but they are **highly structured and semantically meaningful**:

- **Road (40):** +11.6%  
- **Sidewalk (48):** +7.6%  
- **Class 81:** +5.2%  
- **Building (50):** +0.4%  
- **Car (10):** small positive gain  
- **Vegetation (70):** -3.6%

The most significant improvements occur in **dominant, spatially consistent classes** such as road and sidewalk, which are central to driving scenes. In particular, the **+11.6% gain on the road class** represents a substantial shift in discriminability for one of the most critical semantic categories.

The modest global average reflects a **mixture of strong gains and weaker or negative cases**, rather than weak performance. This aligns with the broader findings of the work: reflectivity-aware augmentation produces **clear benefits in structured, stable regions**, while remaining sensitive to noisy or highly variable classes.

Overall, the result is not a uniform boost, but a **targeted and interpretable improvement pattern**, where the proxy meaningfully enhances key scene elements without introducing artificial uniform gains.

---

## Final Modular Code Path

The final repository is not only notebook-based. It is also modularized through `src/`.

### `src/io/`

Handles data loading and sequence sampling.

> `loader.py`: frame loading

> `sequence_sampler.py`: contiguous window selection

### `src/signals/`

Builds reflectivity-aware features.

> `reflectivity.py`: core signal construction logic

### `src/metrics/`

Numerical evaluation layer.

> `separability.py`: Fisher-style semantic separability

> `csv_logger.py`: run logging to CSV

### `src/semantics/`

Semantic bookkeeping.

> `class_stats.py`

> `label_map.py`

### `src/visualization/`

Frame rendering logic for artifacts.

> `frame_renderer.py`

### `src/animation/`

Temporal artifact writer.

> `gif_writer.py`

This modular path is one of the biggest engineering upgrades over the midterm.

---

## **How to Generate the Final GIF**

### 1. (Optional) Create artifacts directory

If the `artifacts/` folder does not exist, create it first:

```bash
mkdir -p artifacts
```

### 2. Run the pipeline

```bash
python scripts/generate_gif.py \
  --dataset data/semantickitti/dataset \
  --fps 10 \
  --duration 60 \
  --output artifacts/final_seq.gif \
  --sequences 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21
```

### 3. Customizing the run

You can modify parameters depending on your needs:

#### Duration
- 60 seconds → `--duration 60`
- 30 seconds → `--duration 30`

#### FPS (smoothness vs speed)
- Default → `--fps 10`
- Faster → `--fps 15`
- Slower → `--fps 5`

#### Sequence selection
- Single sequence:
  ```bash
  --sequences 00
  ```
- Multiple sequences:
  ```bash
  --sequences 00 09
  ```
- Full range:
  ```bash
  --sequences 00 01 ... 21
  ```

### 4. Output

- GIF: `artifacts/final_seq.gif`
- CSV (auto-generated): `artifacts/final_seq.csv`

The pipeline samples a **contiguous frame window** from the allowed sequences and generates:
- a visual artifact (GIF)
- and a quantitative log (CSV)

Each run may produce a **different sequence window**, depending on the sampling.

### What this does

The script:

1. Samples a contiguous sequence window.
2. Loads each frame.
3. Computes reflectivity-aware signals.
4. Computes per-frame raw and augmented separability.
5. Logs results to CSV.
6. Renders frame boards.
7. Writes the final GIF.

### Duration logic

The script uses:

`window = fps * duration`

So with:

- `fps = 10`
- `duration = 60`

it produces:

- **600 frames total**
- corresponding to a **60-second GIF at 10 FPS**

---

## Generated Artifact Format

#### Preview Artifact

![Final Sequence Artifact](artifacts/final_seq.gif)

The 60-second run produces:

> `artifacts/final_seq.gif`

> `artifacts/final_seq.csv`

### CSV columns

| Column | Meaning |
|---|---|
| `frame_id` | Frame index within the sampled sequence |
| `sequence` | Sequence ID used in the sampled run |
| `sep_raw` | Raw-intensity Fisher-style separability |
| `sep_aug` | Augmented separability using pseudo-reflectivity |
| `delta` | `sep_aug - sep_raw` |

### GIF board layout

The generated board shows:

- **Left:** BEV visualization.
- **Center:** Forward/FOV view (FPS-like sensor-view rendering).
- **Right:** top-class statistics panel.

This matches the visual style shown in the provided artifact screenshot.

---

## Final Artifact (Author's) Run Results from `final_seq.csv`

The provided CSV is especially useful because it is a concrete, run-level summary of the final artifact generation pipeline.

### Aggregate statistics from the CSV

| Metric | Value |
|---|---:|
| Mean raw separability | 0.301838 |
| Mean augmented separability | 0.345452 |
| Mean delta (`aug - raw`) | **+ 0.043614** |
| Relative mean gain vs raw mean | **about + 14.45%** |
| Positive-gain frames | **400 / 600** |
| Negative-gain frames | **200 / 600** |
| Zero-gain frames | 0 |

### Best and worst frames in the provided run

| Case | Frame | Raw | Augmented | Delta |
|---|---:|---:|---:|---:|
| Best gain | 000743 | 0.488249 | 0.949593 | **+ 0.461344** |
| Worst gain | 000355 | 0.664987 | 0.238274 | **- 0.426713** |

### Interpretation of the (author generated) CSV Artifact

The CSV captures frame-wise semantic separability scores for both raw intensity and pseudo-reflectivity across a sampled sequence window.

The results do not show uniform improvement. Instead, they exhibit a clear and structured pattern:

- pseudo-reflectivity improves separability in a majority of frames,
- delivers stronger gains under specific scene conditions,
- and produces negative gains in a smaller subset of cases.

This behavior is consistent with the core findings: reflectivity-aware augmentation introduces meaningful and measurable signal changes, whose impact is governed by scene structure and measurement geometry, rather than acting as a uniformly dominant feature.

This makes the artifact-level result consistent with the broader conclusion:

> Reflectivity-aware augmentation provides measurable benefits, with effectiveness governed by scene structure and measurement conditions.

---

## Why Reflectivity Was Important Here

Reflectivity was important because raw LiDAR intensity alone is strongly influenced by range and measurement geometry, which can obscure meaningful differences between scene elements. By introducing a range-aware term, the proxy reshapes the signal in a way that can improve semantic separability.

In effect:

- raw intensity captures the strength of the measured return,
- pseudo-reflectivity adjusts this signal to partially account for distance, revealing more structured variation across the scene.

This distinction becomes most relevant when:

- geometry alone is insufficient to separate classes,
- surfaces exhibit consistent but subtle response differences,
- or distant elements become attenuated under raw intensity.

Accordingly, the work consistently observed stronger gains for structured classes such as **road** and **sidewalk**, while more irregular and heterogeneous classes such as **vegetation** remained challenging.

---

## Results Summary

The results are based on the provided CSV artifact generated from a sampled multi-sequence run.

| Metric | Value |
|---|---|
| Mean separability gain (proxy − raw) | + 0.0436 |
| Positive-gain frames | 400 / 600 |
| Negative-gain frames | 200 / 600 |
| Overall behavior | Structured, non-uniform improvement |

### Key observation

The results show that pseudo-reflectivity provides **consistent average improvement**, with gains observed in a majority of frames. At the same time, performance is not uniform, and a subset of frames exhibits negative gains.

This confirms that reflectivity-aware augmentation introduces **measurable but context-dependent improvements**, rather than a uniform performance increase across all conditions.

---

## Methodological and Experimental Improvements

The final work extends the initial feasibility study into a more comprehensive and rigorously evaluated reflectivity-aware signal analysis framework.

### 1. Expanded evaluation scope

- initial work: localized analysis on a reference frame and short motion windows.  
- extended work: structured multi-window evaluation with broader temporal coverage.  

→ Result: reduced dependence on isolated examples and improved robustness of observations.

### 2. Systematic proxy design

- initial work: evaluation centered on the `I · R` proxy.  
- extended work: comparison of multiple range-aware transformations.  

→ Result: identification of `log(1 + I · R)` as a more stable analysis-side signal, and explicit rejection of overcompensating variants such as `I · R²`.

### 3. Strengthened evaluation methodology

- initial work: demonstrated the existence of semantic gains.  
- extended work: quantified gain variation across frames and windows, including negative cases.  

→ Result: characterization of when and why reflectivity-aware augmentation improves or degrades separability.

### 4. Transition to reproducible pipeline

- initial work: notebook-driven exploration.  
- extended work: modularized implementation (`src/`, `scripts/`) with reproducible execution and artifact generation.  

→ Result: improved engineering quality, reproducibility, and extensibility.

### 5. Validation of practical utility

- initial work: signal-level analysis.  
- extended work: lightweight downstream evaluation using a simple classifier.  

→ Result: confirmation that reflectivity-aware features provide usable improvements at the feature level, beyond analytical observations.

---

## Limitations and Scope Constraints

This study isolates the effect of range-aware transformations on LiDAR intensity, without extending into full reflectivity reconstruction or material-level inference.

### Scientific scope constraints

- The proxy is not a calibrated reflectivity estimate.
- Material identification is not addressed, as it requires additional modeling beyond range-aware transformations.
- Sensor-specific calibration effects are not explicitly modeled.
- The study does not include a full semantic segmentation training or benchmarking pipeline.
- Improvements are not assumed to be uniform across all scenes or conditions.

### Observed signal limitations

- The direct `I · R` transformation can exhibit instability under certain scene configurations.
- Performance varies across temporal windows and semantic classes.
- Irregular and heterogeneous classes (e.g., vegetation) remain challenging.
- Signal behavior remains influenced by scene structure and measurement geometry.

### Interpretation constraint

Improved visual structure and smoother renderings are used as qualitative indicators of enhanced signal organization. The proxy functions as a controlled, range-aware transformation that improves interpretability and exposes meaningful structure in LiDAR intensity data.

---

## Final Conclusion

**Reflect-Aug-Seg** establishes that a lightweight, range-aware transformation can meaningfully reshape LiDAR intensity into a more informative signal for semantic analysis.

The key outcomes are:

- range-aware augmentation alters signal structure in a measurable way,
- semantic gains emerge consistently, with stronger effects in structured scene elements,
- multi-window evaluation reveals how these gains vary across time and scene composition,
- stabilized transformations improve reliability,
- explicit failure analysis clarifies the limits of the approach,
- and even simple downstream models benefit from the augmented feature.

Taken together, the project demonstrates a complete progression from feasibility to structured evaluation, failure characterization, reproducible artifact generation, and practical validation.

> Reflectivity-aware signal augmentation can serve as a lightweight, physically grounded enhancement to LiDAR-based perception, with measurable benefits and well-characterized behavior across varying conditions.

---

## **Academic Context and Acknowledgment**

This project was completed as part of **SES 598: Space Robotics & AI** at **Arizona State University**, under the guidance of **Prof. Jnaneshwar Das**.

The course is affiliated with the **Distributed Robotic Exploration and Mapping Systems (DREAMS) Laboratory**, whose research focuses on robotic perception, exploration, and autonomous systems.

> **DREAMS Lab Website**: https://deepsig.org/dreamslab  

> **DREAMS Lab GitHub**: https://github.com/DREAMS-lab  

The overall project framing, evaluation discipline, and technical direction were influenced by the course structure and the broader research themes associated with the DREAMS Lab.

This project aligns with core themes in space robotics, including perception, scene understanding, and mapping under uncertainty. By improving the interpretability of LiDAR signals through lightweight transformations, it contributes to more robust environmental understanding, an essential requirement for autonomous exploration, mapping, and decision-making in resource-constrained and extreme environments.

This work represents an independent implementation and analysis carried out within that academic context.

---

## Statement on Use of Generative AI

Generative AI tools (including ChatGPT by OpenAI and Claude by Anthropic) were used during this work to assist with drafting, editing, and improving the clarity and structure of written content, as well as for code organization and debugging support.

All technical decisions, implementations, and results were critically reviewed, validated, and integrated by the author, who assumes full responsibility for the final work.

---

## Special Note on SemanticKITTI

This work relies on the **SemanticKITTI** dataset, an open-source and widely used benchmark for semantic scene understanding with LiDAR sequences.

That dataset is foundational to this work, and this README explicitly acknowledges that dependency because the work would simply not exist without it.

---

## References

### [1] Reflectivity Is All You Need!

Kasi Viswanath, Peng Jiang, and Srikanth Saripalli,  
**“Reflectivity Is All You Need!: Advancing LiDAR Semantic Segmentation,”**  
arXiv preprint arXiv:2403.13188, 2024.  
Paper: <https://arxiv.org/abs/2403.13188>

### [2] SemanticKITTI

Jens Behley, Martin Garbade, Andres Milioto, Jan Quenzel, Sven Behnke, Cyrill Stachniss, and Juergen Gall,  
**“SemanticKITTI: A Dataset for Semantic Scene Understanding of LiDAR Sequences,”**  
Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), 2019, pp. 9297–9307.  
Paper: <https://openaccess.thecvf.com/content_ICCV_2019/html/Behley_SemanticKITTI_A_Dataset_for_Semantic_Scene_Understanding_of_LiDAR_Sequences_ICCV_2019_paper.html>

---

## Citation / BibTeX

### BibTeX for Reflectivity Is All You Need

```bibtex
@misc{viswanath2024reflectivityneedadvancinglidar,
      title={Reflectivity Is All You Need!: Advancing LiDAR Semantic Segmentation}, 
      author={Kasi Viswanath and Peng Jiang and Srikanth Saripalli},
      year={2024},
      eprint={2403.13188},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2403.13188}, 
}
```

### BibTeX for SemanticKITTI

**Dataset**: https://semantic-kitti.org/

```bibtex
@misc{behley2019semantickittidatasetsemanticscene,
      title={SemanticKITTI: A Dataset for Semantic Scene Understanding of LiDAR Sequences}, 
      author={Jens Behley and Martin Garbade and Andres Milioto and Jan Quenzel and Sven Behnke and Cyrill Stachniss and Juergen Gall},
      year={2019},
      eprint={1904.01416},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/1904.01416}, 
}
```

---
