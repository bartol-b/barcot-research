from pathlib import Path
from ase.build import fcc111, add_adsorbate
from ase.constraints import FixAtoms
from ase.io import write
from ase.units import Bohr

root = Path.home() / "Pt111_Hydrogen_Adsorption"
calc_root = root / "calculations"
structures = root / "structures"

pt_psp = Path.home() / "SPARC/psps/78_Pt_18_2.2_2.4_pbe_n_v1.0.psp8"
h_psp = Path.home() / "SPARC/psps/01_H_1_1.0_1.0_pbe_v1.0.psp8"

assert pt_psp.is_file()
assert h_psp.is_file()

for layers in [3, 4]:

    slab = fcc111(
        "Pt",
        size=(3, 3, layers),
        a=3.997,
        vacuum=6.0,
        periodic=True
    )

    # Fix bottom two layers
    fixed = [
        i for i, tag in enumerate(slab.get_tags())
        if tag >= layers - 1
    ]

    assert len(fixed) == 18
    slab.set_constraint(FixAtoms(indices=fixed))

    for hydrogen in [False, True]:

        atoms = slab.copy()

        if hydrogen:
            add_adsorbate(
                atoms,
                "H",
                height=1.0,
                position="fcc",
                offset=(1, 1)
            )

        atoms.set_constraint(FixAtoms(indices=fixed))
        atoms.wrap()

        name = f"Pt111_{layers}L"
        if hydrogen:
            name += "_H"
        name += "_RPBE"

        directory = calc_root / name
        directory.mkdir(parents=True, exist_ok=True)

        # Save ASE geometry
        write(structures / f"{name}.traj", atoms)
        write(structures / f"{name}.xyz", atoms)

        # Generate SPARC ion file
        ion = directory / f"{name}.ion"

        with open(ion, "w") as f:
            groups = [
                ("Pt", list(range(9 * layers)), pt_psp, 195.084)
            ]

            if hydrogen:
                groups.append((
                    "H", [9 * layers], h_psp, 1.008
                ))

            for symbol, indices, psp, mass in groups:

                f.write(f"ATOM_TYPE: {symbol}\n")
                f.write(f"PSEUDO_POT: {psp}\n")
                f.write(f"N_TYPE_ATOM: {len(indices)}\n")
                f.write(f"ATOMIC_MASS: {mass}\n")
                f.write("COORD:\n")

                for i in indices:
                    x, y, z = atoms.positions[i] / Bohr
                    f.write(
                        f"{x:.10f} {y:.10f} {z:.10f}\n"
                    )

                f.write("\nRELAX:\n")

                for i in indices:
                    flag = 0 if i in fixed else 1
                    f.write(f"{flag} {flag} {flag}\n")

                f.write("\n")

        # Generate SPARC input file
        inpt = directory / f"{name}.inpt"

        with open(inpt, "w") as f:
            f.write(f"# {name}\n\n")
            f.write("LATVEC_SCALE: 1 1 1\n")
            f.write("LATVEC:\n")

            for vector in atoms.cell.array / Bohr:
                f.write(
                    " ".join(f"{v:.10f}" for v in vector)
                    + "\n"
                )

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

        # Generate Slurm submission script
        sbatch = directory / f"run_{name}.sbatch"

        with open(sbatch, "w") as f:
            f.write(f"""#!/bin/bash
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
""")

        print(
            f"{name}: {len(atoms)} atoms, "
            f"{len(fixed)} fixed, files generated"
        )

print("\nAll four systems prepared.")
