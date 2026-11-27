#!/bin/bash
#SBATCH --job-name=H2_RPBE
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:30:00
#SBATCH --output=H2_RPBE_slurm_%j.out
#SBATCH --error=H2_RPBE_slurm_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module purge
module load intel-oneapi-compilers
module load intel-oneapi-mkl
module load intel-oneapi-mpi

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1

srun -n 1 "$HOME/SPARC/lib/sparc" -name H2_RPBE
