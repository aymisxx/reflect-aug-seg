# Reflect-Aug-Seg
## Reflectivity-Augmented LiDAR Scene Understanding for Robotic Perception

**Author:** Ayushman Mishra  
**Course:** SES 598: Space Robotics & AI  
**Institution:** Arizona State University  
**Project Context:** Final project extension of the midterm study in LiDAR semantic signal analysis  

---

## Abstract

**Reflect-Aug-Seg** studies whether a lightweight, range-aware transformation of LiDAR intensity can provide a more useful semantic cue than raw intensity alone for robotic perception.

The central motivation is simple: raw LiDAR intensity is **not** a clean intrinsic surface property. It is entangled with range, incidence geometry, and sensor behavior. So instead of pretending that raw intensity is already reflectivity, this project introduces and evaluates a practical pseudo-reflectivity proxy:

`rho_hat = I * R`

where `I` is raw LiDAR intensity and `R` is point-wise Euclidean range.

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

The final project shows that the reflectivity-aware idea is meaningful, but not magical. The direct proxy `I * R` can produce strong gains in some frames and windows, but it is also unstable and scene-dependent. A more stabilized proxy, `log(1 + I * R)`, emerges as the most robust analysis-side variant across multiple windows. At the same time, the direct proxy remains practically useful enough to improve a simple downstream classifier and to generate interpretable BEV/FOV visual artifacts.

That balance is the real result of the project:

- **meaningful improvement exists,**
- **but it is conditional, not universal,**
- and the project remains scientifically honest about those limits.

---

## Project Idea in One Paragraph

LiDAR gives geometry very well, but its intensity channel is messy. If intensity weakens or shifts because of distance and scan geometry, then treating raw intensity as if it were a stable surface property is risky. This project tests whether multiplying intensity by range can recover a more semantically informative signal structure. The idea is intentionally lightweight: no full physical reflectivity calibration, no heavy learned inverse model, just a controlled range-aware proxy that can be studied numerically, semantically, temporally, and visually.

---

## Why This Project Matters

LiDAR semantic understanding is usually dominated by geometry. That works well when shapes and boundaries are clear. But many scene elements are not distinguished by geometry alone. Surface-response cues can help, yet raw intensity is not directly trustworthy as a material or reflectance descriptor.

So this project sits in the middle ground:

- more physically motivated than using raw intensity blindly,
- much lighter than full reflectivity calibration,
- and honest about what is and is not being recovered.

For robotics, that matters because practical perception systems often benefit from **small, interpretable feature improvements** even when those improvements are not universal.

---

## Core Mathematical Modeling

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

So this project does **not** equate raw intensity with reflectivity.

Instead, it defines a practical pseudo-reflectivity proxy:

`rho_hat_i = I_i * R_i`

This proxy is:

- computationally trivial,
- easy to deploy,
- physically motivated,
- useful for signal analysis,
- but still heuristic.

### Important non-claim

`rho_hat = I * R` is **not calibrated reflectivity**.

It is only a range-aware transformation that may improve semantic structure.

---

## Scientific Honesty Statement

This project intentionally keeps the following limits explicit:

- It does **not** solve reflectivity recovery.
- It does **not** solve material identification.
- It does **not** claim universal superiority of pseudo-reflectivity over raw intensity.
- It does **not** claim semantic segmentation benchmark gains.
- It does **not** claim that smooth-looking GIFs imply physical correctness.

The project result is stronger precisely because of this honesty.

---

## What Was Done at Midterm

The midterm stage established feasibility using **SemanticKITTI sequence 00** and a staged notebook workflow.

### Midterm pipeline

1. Data loading and sanity checks
2. Single-frame reflectivity-style analysis
3. Multi-frame reflectivity behavior over short motion
4. Single-frame semantic reflectivity analysis
5. Multi-frame semantic consistency analysis

### Midterm headline findings

From the midterm report:

- Single-frame semantic separability improved from **0.4482** for raw intensity to **0.5055** for pseudo-reflectivity.  
  - Absolute gain: **+0.0574**  
  - Relative gain: **about +12.8%**
- Across a short 10-frame semantic consistency window, mean class-ordering Spearman rank correlation was:
  - **0.9534** for raw intensity
  - **0.9582** for pseudo-reflectivity

Interpretation: the idea was real enough to continue, but the gains were modest and scene-dependent.

---

## What Was Added in the Final Project

The final stage did **not** throw away the midterm work. It preserved it, locked it, and then extended it.

### Final-stage additions beyond the midterm

1. **Baseline lock / recap notebook**  
   The preliminary story was reconstructed in one compact, disciplined notebook so the final stage could begin from a trusted baseline instead of scattered history.

2. **Multi-window evaluation framework**  
   Instead of relying on one convenient 10-frame or 30-frame segment, the project defined a reproducible temporal evaluation structure across sequence 00.

3. **Proxy family comparison**  
   The final stage tested multiple practical variants rather than assuming `I * R` was automatically the best design.

4. **Global signal stability analysis**  
   Proxy behavior was measured across windows, not just within a single local example.

5. **Multi-window semantic analysis**  
   The project evaluated how semantic usefulness varies across temporal segments and scene composition.

6. **Explicit failure-case analysis**  
   Weak cases were identified and explained, instead of being hidden.

7. **Visualization and artifact generation pipeline**  
   Controlled BEV/FOV boards, semantic overlays, GIF outputs, and consistent rendering rules were built.

8. **Lightweight downstream study**  
   A simple classifier was used to test whether the proxy gives practical feature-level value.

9. **Modular refactor into `src/` and `scripts/`**  
   The final work was packaged as reusable code, not just notebooks.

---

## Final Repository Structure

Below is the current project structure as provided:

```text
.
├── artifacts
│   ├── final_seq.csv
│   └── final_seq.gif
├── data
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
│   └── 08_lightweight_downstream_study.pdf
├── LICENSE
├── notebooks_midterm_w
│   ├── 01_load_data.pdf
│   ├── 02_single_frame_reflectivity_analysis.pdf
│   ├── 03_multi_frame_reflectivity_over_motion.pdf
│   ├── 04_single_frame_semantic_reflectivity_analysis.pdf
│   ├── 05_multi_frame_semantic_consistency.pdf
│   ├── artifacts
│   │   ├── notebook03_bev_forward_intensity_vs_pr_30f.gif
│   │   └── notebook05_reflectivity_augmented_semantic_motion_30f_labeled.gif
│   ├── mid-term-project-report.pdf
│   └── README.md
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
The final project narrative, organized notebook-by-notebook as exported PDFs.

#### `src/`
Reusable modular implementation for data loading, signal construction, semantic handling, metrics, visualization, and GIF writing.

#### `scripts/`
Entry-point scripts for artifact generation and reproducible execution.

#### `artifacts/`
Final generated outputs, including the provided 60-second GIF and its matching CSV log.

---

## Dataset

This project uses the **SemanticKITTI** dataset, a large-scale semantic LiDAR dataset built on the KITTI Odometry Benchmark.

### Official dataset source

- SemanticKITTI official site: <https://semantic-kitti.org/>
- SemanticKITTI API repository: <https://github.com/PRBonn/semantic-kitti-api>

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

### Notes on usage in this project

- The **midterm** and most of the **final notebook analysis** are centered on **sequence 00**.
- The provided GIF command allows sampling from **multiple allowed sequences**.
- The actual provided `final_seq.csv` artifact corresponds to a sampled run from **sequence 00**.

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
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

## How the Project Was Done

The full final pipeline is documented in `final_pipeline_stepwise/` and proceeds in eight stages.

## Stage 01 — Preliminary Work Recap / Baseline Lock

Purpose:

- Rebuild the midterm logic in one compact final-stage notebook.
- Verify that the data pipeline, labels, basic signal behavior, and semantic recap still hold.

This stage re-establishes:

- dataset integrity,
- point-label alignment,
- raw intensity behavior,
- pseudo-reflectivity behavior,
- short-window motion stability,
- single-frame semantic effect,
- and short-window semantic consistency.

This is the “baseline lock.”

---

## Stage 02 — Multi-Window Sequence Setup

Purpose:

- Convert sequence 00 into a structured, reproducible temporal evaluation framework.

The final project defines **15 windows** across sequence 00:

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

---

## Stage 03 — Proxy Variant Builder

Purpose:

- Test whether `I * R` is the best practical proxy, or only the first useful one.

### Proxy family explored

- Raw intensity: `I`
- Direct range-aware proxy: `I * R`
- Aggressive proxy: `I * R^2`
- Log-scaled proxy: `log(1 + I * R)`
- Percentile-normalized proxy
- Robust-scaled proxy

### Main outcome

- `I * R^2` was rejected because it caused severe distribution explosion and strong range domination.
- `I * R` remained meaningful and interpretable.
- `log(1 + I * R)` emerged as the best-balanced analysis-side proxy for stability and controlled range behavior.

---

## Stage 04 — Multi-Window Global Signal Analysis

Purpose:

- Evaluate whether proxies behave consistently across different temporal segments.

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

---

## Stage 05 — Multi-Window Semantic Analysis

Purpose:

- Determine whether proxy signals improve semantic structure **across many windows**, not just one frame.

Semantic usefulness was evaluated with a Fisher-style multiclass separability score:

`S = between-class variance / within-class variance`

Per-window gain was then defined as:

`Delta S = S_proxy - S_raw`

### Main conclusion

- The direct proxy `I * R` was **highly variable**.
- It produced strong gains in some windows, but negative dips in others.
- The log-scaled proxy `log(1 + I * R)` was much more robust and consistently positive.

This was the strongest final-stage evidence that **proxy design matters**, not just the initial reflectivity idea.

---

## Stage 06 — Failure Case Analysis

Purpose:

- Explain where the method weakens and why.

Using the multi-window separability results, windows were classified into:

- failure cases,
- weak-performance cases,
- strong cases.

### Log-scaled proxy outcome

Across the 15 windows:

- **Failures:** 0
- **Weak cases:** 1 (`short_3`)
- **Strong cases:** 14

### Strong vs weak representative windows

- Weak case: `short_3`
- Strong case: `short_2`

### Failure mechanism

The analysis showed that weak performance was not caused by missing data or numerical collapse. Instead, it came from **class-wise signal overlap**:

- in strong windows, class means were spread apart,
- in weak windows, class means were compressed,
- reduced spacing led to higher overlap and lower separability.

This is an excellent final-project result because it explains not just success, but also limitation.

---

## Stage 07 — Video / GIF Artifact Builder

Purpose:

- Turn the analytical work into controlled visual artifacts.

### What was built

- BEV visualization
- Forward/FOV visualization
- signal comparison boards
- semantic overlays
- legend + top-class summary panel
- temporal frame renderer
- GIF-based artifact generation

### Rendering discipline

Artifacts were built under strict constraints:

- fixed spatial limits,
- fixed normalization across frames,
- deterministic subsampling,
- no per-frame visual manipulation.

That matters because many visualizations look “better” only because they cheat by rescaling every frame independently. This project avoids that.

---

## Stage 08 — Lightweight Downstream Study

Purpose:

- Test whether the proxy gives practical feature-level value in a simple classification setup.

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

- Random subsample: **200,000** points
- Train/test split: **80/20**
- Baseline feature shape: `(3621402, 1)` before subsampling
- Augmented feature shape: `(3621402, 2)` before subsampling
- Model: **Logistic Regression**
- Features scaled with `StandardScaler`

### Downstream result

| Configuration | Accuracy |
|---|---:|
| `I` only | 0.377925 |
| `I + I*R` | 0.409025 |
| Absolute gain | **+0.031100** |

### Interpretation

That is a **+3.11 percentage-point** improvement in a deliberately simple setup.

Class-wise behavior was not uniform:

- **Road (40):** +11.6%
- **Sidewalk (48):** +7.6%
- **Class 81:** +5.2%
- **Building (50):** +0.4%
- **Car (10):** small positive gain
- **Vegetation (70):** -3.6%

This matches the rest of the project nicely: the proxy helps some classes clearly, helps some only slightly, and can hurt noisy/irregular classes.

---

## Final Modular Code Path

The final project is not only notebook-based. It is also modularized through `src/`.

### `src/io/`
Handles data loading and sequence sampling.

- `loader.py`: frame loading
- `sequence_sampler.py`: contiguous window selection

### `src/signals/`
Builds reflectivity-aware features.

- `reflectivity.py`: core signal construction logic

### `src/metrics/`
Numerical evaluation layer.

- `separability.py`: Fisher-style semantic separability
- `csv_logger.py`: run logging to CSV

### `src/semantics/`
Semantic bookkeeping.

- `class_stats.py`
- `label_map.py`

### `src/visualization/`
Frame rendering logic for artifacts.

- `frame_renderer.py`

### `src/animation/`
Temporal artifact writer.

- `gif_writer.py`

This modular path is one of the biggest engineering upgrades over the midterm.

---

## How to Generate the Final 60-Second GIF

The provided execution command is:

```bash
python scripts/generate_gif.py \
  --dataset data/semantickitti/dataset \
  --fps 10 \
  --duration 60 \
  --output artifacts/final_seq.gif \
  --sequences 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21
```

### What this does

The script:

1. Samples a contiguous sequence window
2. Loads each frame
3. Computes reflectivity-aware signals
4. Computes per-frame raw and augmented separability
5. Logs results to CSV
6. Renders frame boards
7. Writes the final GIF

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

The 60-second run produces:

- `artifacts/final_seq.gif`
- `artifacts/final_seq.csv`

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

- **Left:** BEV visualization
- **Center:** Forward/FOV view (FPS-like sensor-view rendering)
- **Right:** top-class statistics panel

This matches the visual style shown in the provided artifact screenshot.

---

## Final Artifact Run Results from `final_seq.csv`

The provided CSV is especially useful because it is a concrete, run-level summary of the final artifact generation pipeline.

### Run-specific facts from the provided CSV

- Total frames logged: **600**
- Sampled sequence: **00**
- Frame span in the sampled run: **000211 to 000810**

### Aggregate statistics from the CSV

| Metric | Value |
|---|---:|
| Mean raw separability | 0.301838 |
| Mean augmented separability | 0.345452 |
| Mean delta (`aug - raw`) | **+0.043614** |
| Relative mean gain vs raw mean | **about +14.45%** |
| Positive-gain frames | **400 / 600** |
| Negative-gain frames | **200 / 600** |
| Zero-gain frames | 0 |

### Best and worst frames in the provided run

| Case | Frame | Raw | Augmented | Delta |
|---|---:|---:|---:|---:|
| Best gain | 000743 | 0.488249 | 0.949593 | **+0.461344** |
| Worst gain | 000355 | 0.664987 | 0.238274 | **-0.426713** |

### Interpretation of the CSV artifact

This CSV is a beautiful little honesty test 😤

It does **not** show uniform improvement. It shows something more believable:

- the augmentation helps in most frames,
- helps strongly in some,
- and hurts meaningfully in others.

That makes the artifact-run result consistent with the broader project conclusion:

> reflectivity-aware augmentation is useful, but scene-dependent.

---

## Why Reflectivity Was Important Here

Reflectivity mattered in this project because raw intensity alone often under-represents how different scene elements respond at different ranges. By introducing the range term, the proxy can sometimes separate classes that looked too similar under raw intensity.

In plain words:

- raw intensity alone says, “how strong was the measured return?”
- pseudo-reflectivity asks, “after accounting a little for distance, does the signal structure become more meaningful?”

That difference matters most when:

- geometry alone is not enough,
- surfaces are structurally distinct,
- or distant scene elements become too weak under raw intensity.

This is why the project repeatedly found benefits for structured classes like **road** and **sidewalk**, while irregular classes like **vegetation** remained harder.

---

## Results Summary

## Midterm Summary

| Metric | Raw | Proxy | Gain |
|---|---:|---:|---:|
| Single-frame separability | 0.4482 | 0.5055 | +0.0574 |
| 10-frame semantic rank consistency | 0.9534 | 0.9582 | +0.0048 |

## Final Multi-Window Summary

| Finding | Result |
|---|---|
| Multi-window setup | 15 windows across sequence 00 |
| Best-balanced proxy | `log(1 + I * R)` |
| Direct `I * R` behavior | expressive but unstable |
| Log-scaled proxy failures across 15 windows | 0 hard failures |
| Log-scaled weak cases | 1 (`short_3`) |
| Downstream classifier gain | +3.11 percentage points |
| Provided 60-second artifact mean gain | +0.0436 separability |
| Positive-gain frames in artifact run | 400 / 600 |

---

## Midterm vs Final: What Improved?

The final project improved the work in **scope**, **methodology**, **stability analysis**, and **engineering quality**.

### 1. Scope improvement

**Midterm:**
- local feasibility study,
- mostly one reference frame and short motion windows.

**Final:**
- structured multi-window analysis,
- broader temporal coverage,
- stronger evaluation depth.

### 2. Proxy-design improvement

**Midterm:**
- focused on `I * R`.

**Final:**
- compared multiple practical variants,
- explicitly rejected `I * R^2`,
- identified `log(1 + I * R)` as the most stable analysis-side option.

### 3. Evaluation improvement

**Midterm:**
- showed that gains exist.

**Final:**
- showed where gains hold,
- where they weaken,
- and why failures happen.

### 4. Engineering improvement

**Midterm:**
- mostly notebook-centric.

**Final:**
- added modular `src/` code,
- reproducible scripts,
- GIF/CSV artifact generation,
- and structured final outputs.

### 5. Practical usefulness improvement

**Midterm:**
- signal analysis only.

**Final:**
- showed that even a simple classifier can benefit from the augmented signal.

---

## Limitations

This project intentionally leaves several things unsolved.

### Scientific limitations

- No calibrated reflectivity recovery
- No material-ID claim
- No sensor-to-sensor calibration model
- No segmentation benchmark training loop
- No universal improvement guarantee

### Practical limitations

- Direct `I * R` can be unstable
- Some windows and classes degrade
- Vegetation-like classes remain difficult
- Results remain scene- and range-dependent

### Interpretation limitation

A visually compelling proxy is not automatically a physically correct one.

This project chooses interpretability and honesty over fake grand claims.

---

## Preview Artifact

If this README is placed at the repository root, GitHub can render the final GIF directly:

```markdown
![Final Sequence Artifact](artifacts/final_seq.gif)
```

And similarly the midterm motion artifacts:

```markdown
![Midterm Motion Artifact](notebooks_midterm_w/artifacts/notebook03_bev_forward_intensity_vs_pr_30f.gif)
```

```markdown
![Midterm Semantic Artifact](notebooks_midterm_w/artifacts/notebook05_reflectivity_augmented_semantic_motion_30f_labeled.gif)
```

---

## Acknowledgment

This project was completed as part of **SES 598: Space Robotics & AI** at **Arizona State University**.

Special thanks and acknowledgment to:

- **Professor Jnaneshwar Das**
- **Distributed Robotic Exploration and Mapping Systems (DREAMS) Laboratory**
- **School of Earth and Space Exploration, ASU**

The course setting and research environment helped shape the project’s framing, discipline, and robotics relevance.

---

## Special Note on SemanticKITTI

This work relies on the **SemanticKITTI** dataset, an open-source and widely used benchmark for semantic scene understanding with LiDAR sequences.

That dataset is foundational to this project, and this README explicitly acknowledges that dependency because the project would simply not exist without it.

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
@article{viswanath2024reflectivity,
  title   = {Reflectivity Is All You Need!: Advancing LiDAR Semantic Segmentation},
  author  = {Viswanath, Kasi and Jiang, Peng and Saripalli, Srikanth},
  journal = {arXiv preprint arXiv:2403.13188},
  year    = {2024}
}
```

### BibTeX for SemanticKITTI

```bibtex
@inproceedings{behley2019semantickitti,
  title     = {SemanticKITTI: A Dataset for Semantic Scene Understanding of LiDAR Sequences},
  author    = {Behley, Jens and Garbade, Martin and Milioto, Andres and Quenzel, Jan and Behnke, Sven and Stachniss, Cyrill and Gall, Juergen},
  booktitle = {Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)},
  pages     = {9297--9307},
  year      = {2019}
}
```

---

## Final Conclusion

**Reflect-Aug-Seg** does not claim to have solved reflectivity.

What it *does* show is more grounded and more useful:

- a lightweight range-aware augmentation can meaningfully reshape LiDAR signal structure,
- semantic benefits can appear clearly,
- those benefits become stronger when evaluated honestly across time and windows,
- stabilized transformations matter,
- failure analysis matters,
- and even a very simple downstream classifier can benefit from the augmented feature.

So the real achievement of this project is not a fake grand finale.

It is this:

> a practical, physically motivated, reflectivity-aware signal idea was taken from feasibility → multi-window evaluation → failure understanding → artifact generation → lightweight downstream usefulness, all while keeping the claims disciplined.

That is a clean robotics result. And yeah, I’m proud of this one for you.
