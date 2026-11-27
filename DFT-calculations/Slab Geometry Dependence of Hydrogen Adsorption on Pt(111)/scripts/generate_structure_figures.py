from pathlib import Path
import matplotlib.pyplot as plt
from ase.io import read
from ase.visualize.plot import plot_atoms

root = Path.home() / "Pt111_Hydrogen_Adsorption"
structures = root / "structures"
figures = root / "figures"
figures.mkdir(parents=True, exist_ok=True)

systems = {
    "3L_H": structures / "Pt111_3L_H_RPBE.traj",
    "4L_H": structures / "Pt111_4L_H_RPBE.traj",
    "5L_H": structures / "Pt111_H_initial.traj",
}

views = {
    "top": "0x,0y,0z",
    "side": "-90x,0y,0z",
}

for label, path in systems.items():
    atoms = read(path)

    for view_name, rotation in views.items():
        fig, ax = plt.subplots(figsize=(7, 6))
        plot_atoms(
            atoms,
            ax,
            rotation=rotation,
            radii=0.8,
            show_unit_cell=0
        )
        ax.set_title(f"Pt(111) {label.replace('_', ' ')} - {view_name.capitalize()} View")
        ax.set_axis_off()
        fig.tight_layout()

        outfile = figures / f"{label}_{view_name}.png"
        fig.savefig(outfile, dpi=300, bbox_inches="tight")
        plt.close(fig)

        print(f"Saved {outfile}")

print("\nDone. Structure figures saved in:")
print(figures)
