# Slab Geometry Dependence of Hydrogen Adsorption on Pt(111)

**Georgia Institute of Technology | Medford Group | VIP Big Data & Quantum Mechanics**

## Research Objective

Investigate how Pt(111) slab geometry influences hydrogen adsorption energy.

## Computational Methodology

- DFT software: SPARC
- Structure generation and visualization: ASE
- Exchange-correlation functional: RPBE
- HPC cluster: Georgia Tech PACE ICE
- Surface: Pt(111), 3 × 3 supercell
- Slab thicknesses: 3, 4, 5, and 6 layers
- Adsorption site: FCC hollow
- Bottom two Pt layers fixed during relaxation
- K-point grid: 3 × 3 × 1

Both clean and hydrogen-adsorbed Pt(111) slabs were relaxed.

Adsorption energies were calculated using:

E_ads = E(Pt+H) - E(Pt) - 1/2E(H2)

Negative adsorption energies indicate energetically favorable adsorption relative to the molecular hydrogen reference.

