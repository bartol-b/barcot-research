from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ase.io import read
from ase.visualize.plot import plot_atoms
from ase.units import Bohr

root = Path.home() / "Pt111_Hydrogen_Adsorption"
calc = root / "calculations"
structures = root / "structures"
figures = root / "figures"

figures.mkdir(exist_ok=True)

systems = [
    ("3L_H", "Pt111_3L_H_RPBE", structures / "Pt111_3L_H_RPBE.traj"),
    ("4L_H", "Pt111_4L_H_RPBE", structures / "Pt111_4L_H_RPBE.traj"),
    ("5L_H", "Pt111_H_RPBE",    structures / "Pt111_H_initial.traj"),
    ("6L_H", "Pt111_6L_H_RPBE", structures / "Pt111_6L_H_RPBE.traj"),
]

views = {
    "top": "0x,0y,0z",
    "side": "-90x,0y,0z",
}

for label, calc_name, traj_path in systems:
    atoms = read(traj_path)
    n_atoms = len(atoms)

    geopt = calc / calc_name / f"{calc_name}.geopt"
    lines = geopt.read_text().splitlines()

    markers = [i for i, line in enumerate(lines) if line.strip() == ":R(Bohr):"]
    if not markers:
        raise RuntimeError(f"No :R(Bohr): block found in {geopt}")

    start = markers[-1] + 1
    coords_bohr = np.array([
        [float(x) for x in lines[i].split()]
        for i in range(start, start + n_atoms)
    ])

    atoms.positions = coords_bohr * Bohr

    for view_name, rotation in views.items():
        fig, ax = plt.subplots(figsize=(7, 5.5))
        plot_atoms(
            atoms,
            ax,
            rotation=rotation,
            radii=0.8,
            show_unit_cell=0
        )
        ax.set_title(f"Relaxed Pt(111) {label} - {view_name.capitalize()} View")
        ax.set_axis_off()
        fig.tight_layout()

        out = figures / f"{label}_relaxed_{view_name}.png"
        fig.savefig(out, dpi=300, bbox_inches="tight")
        plt.close(fig)
        print("Saved:", out)

print("\nDone.")
