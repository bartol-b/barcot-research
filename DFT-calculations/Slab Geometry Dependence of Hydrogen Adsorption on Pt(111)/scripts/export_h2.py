
from ase.io import read
from ase.units import Bohr
from pathlib import Path

root = Path.home() / "Pt111_Hydrogen_Adsorption"

atoms = read(root / "structures/H2.traj")
positions = atoms.get_positions() / Bohr

psp = (
    Path.home()
    / "SPARC/psps/01_H_1_1.0_1.0_pbe_v1.0.psp8"
)

output = root / "calculations/H2/H2.ion"

with open(output, "w") as f:
    f.write("ATOM_TYPE: H\n")
    f.write(f"PSEUDO_POT: {psp}\n")
    f.write("N_TYPE_ATOM: 2\n")
    f.write("COORD:\n")

    for x, y, z in positions:
        f.write(f"{x:.10f} {y:.10f} {z:.10f}\n")

print(f"Created {output}")
print("Initial H-H bond length:",
      atoms.get_distance(0, 1), "Angstrom")
