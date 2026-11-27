from pathlib import Path
import numpy as np
from ase.io import read, write
from ase.build import add_adsorbate
from ase.constraints import FixAtoms
from ase.units import Bohr

# Project directories
root = Path.home() / "Pt111_Hydrogen_Adsorption"
clean = root / "calculations/Pt111_clean_RPBE"
output = root / "calculations/Pt111_H_RPBE"
output.mkdir(parents=True, exist_ok=True)

# Load original ASE slab
atoms = read(root / "structures/Pt111_clean.traj")
assert len(atoms) == 45

# Identify fixed Pt atoms
fixed = set()
for constraint in atoms.constraints:
    if isinstance(constraint, FixAtoms):
        fixed.update(constraint.get_indices())

assert len(fixed) == 18

# Read final relaxed Pt positions from SPARC
lines = (clean / "Pt111_clean_RPBE.geopt").read_text().splitlines()

markers = [
    i for i, line in enumerate(lines)
    if line.strip() == ":R(Bohr):"
]

assert markers, "No geometry found"

start = markers[-1] + 1

coordinates = np.array([
    [float(x) for x in lines[i].split()]
    for i in range(start, start + 45)
])

assert coordinates.shape == (45, 3)

atoms.positions = coordinates * Bohr

# Verify ASE retains adsorption-site metadata
assert "adsorbate_info" in atoms.info, (
    "ASE slab adsorption-site metadata missing"
)
assert "fcc" in atoms.info["adsorbate_info"].get("sites", {}), (
    "FCC hollow adsorption site unavailable"
)

# Add hydrogen at FCC hollow site
add_adsorbate(
    atoms,
    "H",
    height=1.0,
    position="fcc",
    offset=(1, 1)
)

assert len(atoms) == 46
assert atoms[-1].symbol == "H"

# Bottom two Pt layers fixed; other atoms relaxed
atoms.set_constraint(FixAtoms(indices=sorted(fixed)))

# Wrap into periodic simulation cell
atoms.wrap()

# Save ASE structure
write(root / "structures/Pt111_H_initial.traj", atoms)

# Pseudopotentials
pt_psp = Path.home() / (
    "SPARC/psps/78_Pt_18_2.2_2.4_pbe_n_v1.0.psp8"
)

h_psp = Path.home() / (
    "SPARC/psps/01_H_1_1.0_1.0_pbe_v1.0.psp8"
)

assert pt_psp.is_file()
assert h_psp.is_file()

# Generate SPARC ion file
ion_path = output / "Pt111_H_RPBE.ion"
positions = atoms.positions / Bohr

with open(ion_path, "w") as f:
    for symbol, indices, psp, mass in [
        ("Pt", range(45), pt_psp, 195.084),
        ("H", range(45, 46), h_psp, 1.008)
    ]:
        f.write(f"ATOM_TYPE: {symbol}\n")
        f.write(f"PSEUDO_POT: {psp}\n")
        f.write(f"N_TYPE_ATOM: {len(indices)}\n")
        f.write(f"ATOMIC_MASS: {mass}\n")
        f.write("COORD:\n")

        for i in indices:
            x, y, z = positions[i]
            f.write(f"{x:.10f} {y:.10f} {z:.10f}\n")

        f.write("\nRELAX:\n")

        for i in indices:
            flag = 0 if i in fixed else 1
            f.write(f"{flag} {flag} {flag}\n")

        f.write("\n")

# Generate SPARC input file
input_path = output / "Pt111_H_RPBE.inpt"
cell = atoms.cell.array / Bohr

with open(input_path, "w") as f:
    f.write("# H adsorption at FCC hollow on Pt(111)\n\n")
    f.write("LATVEC_SCALE: 1 1 1\n")
    f.write("LATVEC:\n")

    for vector in cell:
        f.write(" ".join(f"{v:.10f}" for v in vector))
        f.write("\n")

    f.write("\nBC: P P D\n")
    f.write("EXCHANGE_CORRELATION: GGA_RPBE\n")
    f.write("KPOINT_GRID: 3 3 1\n")
    f.write("ELEC_TEMP_TYPE: fd\n")
    f.write("SMEARING: 0.003674932\n")
    f.write(f"MESH_SPACING: {0.20 / Bohr:.8f}\n")
    f.write("FD_ORDER: 12\n")
    f.write("TOL_SCF: 1e-5\n")
    f.write("RELAX_FLAG: 1\n")
    f.write("RELAX_METHOD: LBFGS\n")
    f.write("TOL_RELAX: 3.89e-4\n")
    f.write("PRINT_FORCES: 1\n")
    f.write("PRINT_ATOMS: 1\n")
    f.write("PRINT_RELAXOUT: 1\n")

# Confirm structure
print("\nSPARC input files generated successfully!")
print("Total atoms:", len(atoms))
print("Fixed Pt atoms:", len(fixed))
print("Relaxing atoms:", len(atoms) - len(fixed))
print("Hydrogen position (Angstrom):", atoms[-1].position)
print("Pt surface max z (Angstrom):", max(atoms.positions[:45, 2]))
print("Output directory:", output)
