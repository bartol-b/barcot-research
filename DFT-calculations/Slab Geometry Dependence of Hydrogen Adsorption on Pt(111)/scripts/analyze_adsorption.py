from pathlib import Path
import re
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path.home() / "Pt111_Hydrogen_Adsorption"
calc = root / "calculations"
results = root / "results"
figures = root / "figures"

results.mkdir(exist_ok=True)
figures.mkdir(exist_ok=True)

HA_TO_EV = 27.211386245988

def get_energy(name):
    path = calc / name / f"{name}.out"

    if not path.exists():
        print(f"{name}: output not available")
        return None

    text = path.read_text()

    # Avoid extracting intermediate energies from running jobs
    if "Total walltime" not in text:
        print(f"{name}: calculation not finished")
        return None

    energies = re.findall(
        r"Total free energy\s*:\s*([+-]?\d+\.?\d*[Ee][+-]?\d+)",
        text
    )
    forces = re.findall(
        r"Maximum force\s*:\s*([+-]?\d+\.?\d*[Ee][+-]?\d+)",
        text
    )

    if not energies or not forces:
        print(f"{name}: missing energy or force data")
        return None

    energy = float(energies[-1])
    force = float(forces[-1])

    tolerance = 3.89e-4
    if force > tolerance:
        print(f"{name}: final force exceeds tolerance ({force:.3e})")
        return None

    print(f"{name}: {energy:.10f} Ha, Fmax={force:.3e}")
    return energy

# Prefer refined H2 calculation
h2 = get_energy("H2_RPBE_relaxed_grid144")

if h2 is None:
    print("Refined H2 energy unavailable; analysis deferred.")
    raise SystemExit(0)

rows = []

for layers in [3, 4, 5, 6]:
    if layers == 5:
        clean_name = "Pt111_clean_RPBE"
        ads_name = "Pt111_H_RPBE"
    else:
        clean_name = f"Pt111_{layers}L_RPBE"
        ads_name = f"Pt111_{layers}L_H_RPBE"

    clean = get_energy(clean_name)
    ads = get_energy(ads_name)

    if clean is None or ads is None:
        print(f"{layers} layers: awaiting valid calculations")
        continue

    e_ads = (ads - clean - 0.5 * h2) * HA_TO_EV

    rows.append([layers, clean, ads, h2, e_ads])
    print(f"{layers} layers: E_ads = {e_ads:.6f} eV")

csv_path = results / "adsorption_vs_thickness.csv"

with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Layers",
        "Clean_Energy_Ha",
        "Adsorbed_Energy_Ha",
        "H2_Energy_Ha",
        "Adsorption_Energy_eV"
    ])
    writer.writerows(rows)

print(f"\nResults saved: {csv_path}")

if len(rows) >= 2:
    layers = [r[0] for r in rows]
    adsorption = [r[4] for r in rows]

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.plot(layers, adsorption, "o-", linewidth=2)
    ax.axhline(
        y=-0.384,
        color="red",
        linestyle="--",
        linewidth=1.8,
        label="Yu et al. (2018): -0.384 eV"
    )
    ax.legend()
    ax.set_xlabel("Number of Pt(111) Layers")
    ax.set_ylabel("Hydrogen Adsorption Energy (eV)")
    ax.set_title("Hydrogen Adsorption vs. Pt(111) Slab Thickness")
    ax.set_xticks(layers)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    path = figures / "adsorption_vs_thickness.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)

    print(f"Plot saved: {path}")
else:
    print("Awaiting at least two converged slab pairs for plotting.")

print("\nAnalysis finished.")
