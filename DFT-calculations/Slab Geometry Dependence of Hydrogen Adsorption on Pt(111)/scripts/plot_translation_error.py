from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path.home() / "Pt111_Hydrogen_Adsorption"
figures = root / "figures"
figures.mkdir(exist_ok=True)

# H2 fixed-geometry calculations before and after 0.10 Å translation
grid = np.array([75, 87, 120])

energy_original = np.array([
    -1.2011193751,
    -1.1869154172,
    -1.1790275065
])

energy_shifted = np.array([
    -1.1842912793,
    -1.1808838348,
    -1.1789363294
])

HA_TO_EV = 27.211386245988

translation_error = abs(energy_shifted - energy_original) * HA_TO_EV

fig, ax = plt.subplots(figsize=(8, 5))

bars = ax.bar(grid.astype(str), translation_error, width=0.5)

for bar, value in zip(bars, translation_error):
    ax.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 0.01,
        f"{value:.4f} eV",
        ha="center",
        fontsize=11
    )

ax.set_xlabel("Finite-Difference Grid Size (N × N × N)")
ax.set_ylabel("Absolute Energy Difference (eV)")
ax.set_title("H₂ Grid-Position Sensitivity (0.10 Å Translation)")
ax.set_ylim(0, 0.53)
ax.grid(axis="y", alpha=0.3)
ax.set_axisbelow(True)

fig.tight_layout()

output = figures / "translation_error.png"
fig.savefig(output, dpi=300, bbox_inches="tight")
plt.close(fig)

print("Saved:", output)
