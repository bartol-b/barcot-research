
from pathlib import Path
import numpy as np
from ase.io import read
from ase.units import Bohr
from ase.constraints import FixAtoms

# Project directories
root = Path.home() / "Pt111_Hydrogen_Adsorption"
output = root / "calculations/Pt111_clean_RPBE"
output.mkdir(parents=True, exist_ok=True)

# Read previously generated ASE slab
atoms = read(root / "structures/Pt111_clean.traj")

# Convert Angstrom to Bohr (SPARC native units)
cell = atoms.cell.array / Bohr
positions = atoms.positions / Bohr

# Identify fixed atoms
fixed = set()
for constraint in atoms.constraints:
    if isinstance(constraint, FixAtoms):
        fixed.update(constraint.get_indices())

assert len(atoms) == 45
assert len(fixed) == 18

# Platinum pseudopotential
psp = (
    Path.home()
    / "SPARC/psps/"
    "78_Pt_18_2.2_2.4_pbe_n_v1.0.psp8"
)

assert psp.is_file(), "Pt pseudopotential missing"

# Generate atomic positions / relaxation flags
ion_path = output / "Pt111_clean_RPBE.ion"

with open(ion_path, "w") as f:
    f.write("ATOM_TYPE: Pt\n")
    f.write(f"PSEUDO_POT: {psp}\n")
    f.write(f"N_TYPE_ATOM: {len(atoms)}\n")
    f.write("ATOMIC_MASS: 195.084\n")
    f.write("COORD:\n")

    for x, y, z in positions:
        f.write(f"{x:.10f} {y:.10f} {z:.10f}\n")

    f.write("\nRELAX:\n")
    for i in range(len(atoms)):
        flag = 0 if i in fixed else 1
        f.write(f"{flag} {flag} {flag}\n")

# Generate SPARC parameters
input_path = output / "Pt111_clean_RPBE.inpt"

with open(input_path, "w") as f:
    f.write("# Clean Pt(111), 5 layers, 3x3 cell\n")
    f.write("# Preliminary RPBE calculation\n\n")

    f.write("LATVEC_SCALE: 1 1 1\n")
    f.write("LATVEC:\n")

    for vector in cell:
        f.write(" ".join(f"{v:.10f}" for v in vector))
        f.write("\n")

    f.write("\n")
    f.write("BC: P P D\n")
    f.write("EXCHANGE_CORRELATION: GGA_RPBE\n")
    f.write("KPOINT_GRID: 3 3 1\n")

    # Electronic occupations for metallic Pt
    f.write("ELEC_TEMP_TYPE: fd\n")
    f.write("SMEARING: 0.003674932\n")

    # Preliminary real-space grid
    spacing = 0.20 / Bohr
    f.write(f"MESH_SPACING: {spacing:.8f}\n")
    f.write("FD_ORDER: 12\n")

    f.write("TOL_SCF: 1e-5\n")
    f.write("RELAX_FLAG: 1\n")
    f.write("RELAX_METHOD: LBFGS\n")
    f.write("TOL_RELAX: 3.89e-4\n")

    f.write("PRINT_FORCES: 1\n")
    f.write("PRINT_ATOMS: 1\n")
    f.write("PRINT_RELAXOUT: 1\n")

print("SPARC input files generated.")
print("Atoms:", len(atoms))
print("Fixed atoms:", len(fixed))
print("Input:", input_path)
print("Ions:", ion_path)
print("Cell vectors in Bohr:")
print(cell)
