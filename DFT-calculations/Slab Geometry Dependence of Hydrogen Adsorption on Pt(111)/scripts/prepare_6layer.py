from pathlib import Path
from ase.build import fcc111, add_adsorbate
from ase.constraints import FixAtoms
from ase.io import write
from ase.units import Bohr

root = Path.home() / "Pt111_Hydrogen_Adsorption"
calc = root / "calculations"
structures = root / "structures"

layers = 6
slab = fcc111(
    "Pt", size=(3, 3, layers),
    a=3.997, vacuum=6.0, periodic=True
)

fixed = [
    i for i, tag in enumerate(slab.get_tags())
    if tag >= layers - 1
]
assert len(fixed) == 18
slab.set_constraint(FixAtoms(indices=fixed))

pt_psp = Path.home() / (
    "SPARC/psps/78_Pt_18_2.2_2.4_pbe_n_v1.0.psp8"
)
h_psp = Path.home() / (
    "SPARC/psps/01_H_1_1.0_1.0_pbe_v1.0.psp8"
)
assert pt_psp.is_file() and h_psp.is_file()

for hydrogen in [False, True]:
    atoms = slab.copy()

    if hydrogen:
        add_adsorbate(
            atoms, "H", height=1.0,
            position="fcc", offset=(1, 1)
        )

    atoms.set_constraint(FixAtoms(indices=fixed))
    atoms.wrap()

    name = "Pt111_6L_H_RPBE" if hydrogen else "Pt111_6L_RPBE"
    directory = calc / name

    if directory.exists() and any(directory.iterdir()):
        raise RuntimeError(f"Existing files detected: {directory}")

    directory.mkdir(parents=True, exist_ok=True)

    write(structures / f"{name}.traj", atoms)
    write(structures / f"{name}.xyz", atoms)

    with open(directory / f"{name}.ion", "w") as f:
        groups = [
            ("Pt", range(54), pt_psp, 195.084)
        ]
        if hydrogen:
            groups.append(("H", range(54, 55), h_psp, 1.008))

        for symbol, indices, psp, mass in groups:
            f.write(f"ATOM_TYPE: {symbol}\n")
            f.write(f"PSEUDO_POT: {psp}\n")
            f.write(f"N_TYPE_ATOM: {len(indices)}\n")
            f.write(f"ATOMIC_MASS: {mass}\n")
            f.write("COORD:\n")

            for i in indices:
                x, y, z = atoms.positions[i] / Bohr
                f.write(f"{x:.10f} {y:.10f} {z:.10f}\n")

            f.write("\nRELAX:\n")
            for i in indices:
                flag = 0 if i in fixed else 1
                f.write(f"{flag} {flag} {flag}\n")
            f.write("\n")

    with open(directory / f"{name}.inpt", "w") as f:
        f.write(f"# {name}\n\n")
        f.write("LATVEC_SCALE: 1 1 1\n")
        f.write("LATVEC:\n")

        for v in atoms.cell.array / Bohr:
            f.write(" ".join(f"{x:.10f}" for x in v) + "\n")

        f.write("\nBC: P P D\n")
        f.write("EXCHANGE_CORRELATION: GGA_RPBE\n")
        f.write("KPOINT_GRID: 3 3 1\n")
        f.write("ELEC_TEMP_TYPE: fd\n")
        f.write("SMEARING: 0.003674932\n")
        f.write("MESH_SPACING: 0.37794523\n")
        f.write("FD_ORDER: 12\n")
        f.write("TOL_SCF: 1e-5\n")
        f.write("RELAX_FLAG: 1\n")
        f.write("RELAX_METHOD: LBFGS\n")
        f.write("TOL_RELAX: 3.89e-4\n")
        f.write("PRINT_FORCES: 1\n")
        f.write("PRINT_ATOMS: 1\n")
        f.write("PRINT_RELAXOUT: 1\n")

    script = f"""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --time=10:00:00
#SBATCH --output=slurm_%j.out
#SBATCH --error=slurm_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module purge
module load intel-oneapi-compilers
module load intel-oneapi-mkl
module load intel-oneapi-mpi

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1

srun -n 8 "$HOME/SPARC/lib/sparc" -name {name}
"""
    (directory / f"run_{name}.sbatch").write_text(script)

    assert len(atoms) == (55 if hydrogen else 54)
    assert len(fixed) == 18

    print(f"{name}: {len(atoms)} atoms, 18 fixed")
    print("Files:", directory)

print("Both six-layer systems prepared successfully.")
