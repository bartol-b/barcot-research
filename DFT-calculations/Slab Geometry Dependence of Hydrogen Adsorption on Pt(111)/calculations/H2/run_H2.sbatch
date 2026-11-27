#!/bin/bash
#SBATCH --job-name=H2_DFT
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:30:00
#SBATCH --output=H2_slurm_%j.out
#SBATCH --error=H2_slurm_%j.err

set -euo pipefail

# Move to the calculation directory
cd "$SLURM_SUBMIT_DIR"

# Load PACE computing modules
module purge
module load intel-oneapi-compilers
module load intel-oneapi-mkl
module load intel-oneapi-mpi

# Avoid unnecessary threading
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1

# Run SPARC on the allocated compute node
srun -n 1 "$HOME/SPARC/lib/sparc" -name H2
