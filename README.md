# 📡 **reflect-aug-seg** 🫧

**(Reflectivity-Augmented LiDAR Semantic Segmentation for Robust Robotic Perception)**

## Overview

This project explores whether **reflectivity-like features derived from LiDAR intensity** can improve semantic segmentation in robotic perception systems.

Instead of relying purely on geometry and raw intensity, we introduce a **pseudo-reflectivity feature** that compensates for distance-dependent distortions in LiDAR measurements.

---

## Motivation

LiDAR intensity is influenced by:

- Distance from sensor (range).
- Angle of incidence.
- Surface material.

This makes raw intensity **inconsistent** as a feature.

> **Goal**: remove the distance dependency to recover a more intrinsic surface property, **reflectivity**.

## Key Concepts

- **LiDAR Point Cloud** → (x, y, z, intensity).
- **Range (R)** → distance from sensor.
- **Intensity (I)** → returned signal strength.
- **Reflectivity (ρ)** → intrinsic surface property.
- **Semantic Segmentation** → classifying each point.

## Mathematical Formulation

### 1. Point Representation

$$p = (x, y, z, I)$$

### 2. Range Computation

$$R = sqrt(x² + y² + z²)$$

### 3. Physical Relationship

$$I ∝ (ρ · cos(α)) / R²$$

Where:

- $ρ$ → reflectivity.
- $α$ → angle of incidence.
- $R$ → range,

> Intensity is not purely intrinsic.

### 4. Pseudo-Reflectivity (Proposed)

$$ρ̂ = I · R$$

### 5. Normalization

$ρ_{norm} = (ρ̂ - μ) / σ$ or $ρ_{norm} = (ρ̂ - min) / (max - min)$

### 6. Feature Sets

$$X₁ = [x, y, z, I]$$

$$X₂ = [x, y, z, ρ_{norm}]$$

$$X₃ = [x, y, z, I, ρ_{norm}]$$

## Dataset

Primary Dataset: **SemanticKITTI** (subset)

> Dataset is not included in the repository.

## Methodology

1. Load LiDAR data.  
2. Compute range.  
3. Compute pseudo-reflectivity.  
4. Visualize distributions.  
5. Analyze separability.  

## Evaluation Metrics

$σ_c² = Var$ (features in class c)  

$d(c₁, c₂) = ||μ_c₁ - μ_c₂||$

Silhouette Score → higher is better.  
Range Stability → lower variance is better.  

(Final Phase)  

$$IoU = TP / (TP + FP + FN)$$
$$m-IoU = mean-over-classes$$

## Repository Structure

```
reflect-aug-seg/
├── proposal/
│   ├── project_proposal.md                (Preliminary submission)
│   ├── project_proposal.pdf               (Preliminary submission)
│   └── figures/                           (Preliminary submission)
│       ├── intensity_plot.png
│       ├── reflectivity_plot.png
│       └── comparison.png
│
├── notebooks/
│   ├── 01_load_data.ipynb                 (Preliminary submission)
│   └── 02_preliminary_results.ipynb       (Preliminary submission)
│
├── data/
│   └── semantickitti_subset/              (Preliminary use only - not submitted)
│
├── src/
│   ├── load_data.py                       (Preliminary submission)
│   ├── pseudo_reflectivity.py             (Preliminary submission)
│   └── visualize.py                       (Preliminary submission)
│
├── results/
│   ├── intensity_plot.png                 (Preliminary submission)
│   ├── reflectivity_plot.png              (Preliminary submission)
│   └── comparison.png                     (Preliminary submission)
│
├── ros2_pipeline/                         (Final deliverable - not part of preliminary submission)
│   ├── nodes/
│   ├── launch/
│   └── configs/
│
├── models/                                (Final deliverable - not part of preliminary submission)
│   └── trained_segmentation_model.pth
│
└── deployment/                            (Final deliverable - not part of preliminary submission)
    ├── hardware_setup.md
    ├── runtime_results/
    └── performance_logs/
```

## Project Phases

### Phase 1: Preliminary

- Reflectivity computation.  
- Visualization.  
- Analysis.  

### Phase 2: System Development

- Segmentation model.  
- Feature integration.  

### Phase 3: Deployment

- ROS2 pipeline.  
- Real-time processing.  

## Expected Outcomes

- Reduced variance vs intensity.  
- Better class separation.  
- Range-invariant features.  

## Author

### **Ayushman Mishra**  

**Personal-Work**: https://aymisxx.github.io/  
**LinkedIn**: https://www.linkedin.com/in/aymisxx/  
**GitHub-ID**: https://github.com/aymisxx/  

---

## Current Condition: **Under COnstruction**.

---
