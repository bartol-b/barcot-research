#!/bin/bash
#SBATCH --job-name=Pt111_4L_RPBE
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

srun -n 8 "$HOME/SPARC/lib/sparc" -name Pt111_4L_RPBE
