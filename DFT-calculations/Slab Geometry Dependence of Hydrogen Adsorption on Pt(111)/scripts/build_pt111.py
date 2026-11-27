
from ase.build import fcc111, add_adsorbate, molecule
from ase.constraints import FixAtoms
from ase.io import write

# =========================================
# Pt(111) Hydrogen Adsorption - VIP Project
# Reference: Yu et al. (2018)
# =========================================

# Reference geometry
a = 3.997          # Pt lattice constant (Angstrom)
layers = 5         # Number of Pt atomic layers
vacuum = 12.0      # Vacuum gap (Angstrom)
size = (3, 3, layers)

# 1. Construct clean Pt(111) slab
slab = fcc111(

    "Pt",
    size=size,
    a=a,
    vacuum=vacuum / 2,
    periodic=True
)

# Fix bottom two platinum layers
tags = slab.get_tags()
slab.set_constraint(
    FixAtoms(mask=[tag >= layers - 1 for tag in tags])
)

# Save clean slab
write("structures/Pt111_clean.traj", slab)
write("structures/Pt111_clean.xyz", slab)

# 2. Add hydrogen at FCC hollow site
adsorbed = slab.copy()

add_adsorbate(
    adsorbed,
    "H",
    height=1.0,
    position="fcc"
)

write("structures/Pt111_H_fcc.traj", adsorbed)
write("structures/Pt111_H_fcc.xyz", adsorbed)

# 3. Construct isolated H2 molecule
h2 = molecule("H2")
h2.set_cell([15.0, 15.0, 15.0])
h2.center()
h2.pbc = (True, True, True)

write("structures/H2.traj", h2)
write("structures/H2.xyz", h2)

# 4. Verify structures
print("Structures generated successfully!")
print("Clean Pt(111):", len(slab), "atoms")
print("H/Pt(111):", len(adsorbed), "atoms")
print("H2 molecule:", len(h2), "atoms")
print("Fixed Pt atoms:",
      sum(tags >= layers - 1))
