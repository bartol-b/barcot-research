from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path.home() / "Pt111_Hydrogen_Adsorption"
figures = root / "figures"
figures.mkdir(exist_ok=True)

# Fixed-geometry H2 calculations, RPBE
grid = [72, 75, 81, 87, 120, 132, 144]

energy = [
    -1.1810075287,
    -1.2011193751,
    -1.2008923446,
    -1.1869154172,
    -1.1790275065,
    -1.1786277225,
    -1.1785490476
]

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(grid, energy, "o-", linewidth=2, markersize=7)

ax.set_xlabel("Finite-Difference Grid Size (N × N × N)")
ax.set_ylabel("H₂ Total Energy (Ha)")
ax.set_title("H₂ Grid Convergence (RPBE, Fixed Geometry)")
ax.grid(True, alpha=0.3)

fig.tight_layout()

output = figures / "h2_convergence.png"
fig.savefig(output, dpi=300)
plt.close(fig)

print("Saved:", output)
