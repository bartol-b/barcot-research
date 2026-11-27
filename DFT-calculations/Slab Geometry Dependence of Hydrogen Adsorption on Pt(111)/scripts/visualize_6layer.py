from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ase.io import read
from ase.visualize.plot import plot_atoms

root = Path.home() / "Pt111_Hydrogen_Adsorption"
figures = root / "figures"
structures = root / "structures"

for label, name in [
    ("6L_clean", "Pt111_6L_RPBE"),
    ("6L_H", "Pt111_6L_H_RPBE")
]:
    atoms = read(structures / f"{name}.traj")

    for view, rotation in [
        ("top", "0x,0y,0z"),
        ("side", "-90x,0y,0z")
    ]:
        fig, ax = plt.subplots(figsize=(7, 5.5))
        plot_atoms(
            atoms, ax,
            rotation=rotation,
            radii=0.8,
            show_unit_cell=0
        )
        ax.set_title(f"Pt(111) 6 Layers - {label} - {view}")
        ax.set_axis_off()
        fig.tight_layout()

        output = figures / f"{label}_{view}.png"
        fig.savefig(output, dpi=300, bbox_inches="tight")
        plt.close(fig)
        print("Saved:", output)
