# Slab Geometry Dependence of Hydrogen Adsorption on Pt(111)

Computational investigation of hydrogen adsorption on Pt(111) surfaces using density functional theory (DFT).

**Georgia Institute of Technology | VIP Big Data & Quantum Mechanics**

## Research Objective

Investigate how Pt(111) slab thickness influences hydrogen adsorption energy and compare results with published DFT calculations.

## Computational Methodology

- DFT software: SPARC
- Structure generation and visualization: ASE
- Exchange-correlation functional: RPBE
- HPC cluster: Georgia Tech PACE
- Surface: Pt(111), 3 × 3 supercell
- Slab thicknesses: 3, 4, 5, and 6 layers
- Adsorption site: FCC hollow
- Bottom two Pt layers fixed during relaxation
- K-point grid: 3 × 3 × 1

Both clean and hydrogen-adsorbed Pt(111) slabs were relaxed.

## Adsorption Energy

Adsorption energies were calculated using:

E_ads = E(Pt+H) - E(Pt) - 0.5 E(H2)

Negative adsorption energies indicate energetically favorable adsorption relative to the molecular hydrogen reference.

## Results

| Pt(111) Layers | Adsorption Energy (eV/H) |
|---|---:|
| 3 | -0.304655 |
| 4 | -0.286956 |
| 5 | -0.303403 |
| 6 | -0.348854 |

The six-layer slab produced the most negative adsorption energy and the closest agreement with the literature benchmark.

Yu et al. (2018) reported approximately -0.384 eV/H for hydrogen adsorption at the FCC hollow site.

The calculated adsorption energies exhibit non-monotonic thickness dependence. Complete slab-thickness convergence has not been demonstrated.

## Numerical Challenges

The isolated H2 reference calculation exhibited substantial sensitivity to finite-difference grid resolution.

A rigid translation of H2 by 0.10 Å produced large changes in calculated total energy at coarse grid resolutions, indicating an egg-box effect.

Increasing the grid resolution significantly reduced this numerical sensitivity.

The final relaxed H2 calculation used a 144 × 144 × 144 finite-difference grid.

Further convergence testing of slab mesh resolution, vacuum spacing, and k-point density would be required for higher-precision results.

## Repository Contents

- `calculations/` — SPARC input files and Slurm submission scripts
- `scripts/` — Python scripts for structure preparation, visualization, and analysis
- `structures/` — ASE-generated atomic structures
- `results/` — Adsorption energy data
- `figures/` — Atomic visualizations and numerical analysis plots

The SPARC input files contain machine-specific pseudopotential paths that must be adjusted for use on other systems.

## Reference

Yu et al. (2018). *Catalysts*, 8(10), 450.

https://doi.org/10.3390/catal8100450
