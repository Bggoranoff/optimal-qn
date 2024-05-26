#!/bin/bash

#SBATCH --job-name="policy_iter_8links"
#SBATCH --time=10:10:00
#SBATCH --ntasks=1
#SBATCH --partition=compute-p2
#SBATCH --mem-per-cpu=80GB

#SBATCH --cpus-per-task=1
#SBATCH --account=education-eemcs-courses-cse3000
#SBATCH --output=/home/%u/OptimalNearTerm/delftblue/logs/%x_%j.out
#SBATCH --error=/home/%u/OptimalNearTerm/delftblue/logs/%x_%j.err

module load miniconda3

unset CONDA_SHLVL
source "$(conda info --base)/etc/profile.d/conda.sh"

conda activate myenv

srun poetry run policyIter --links 8 --thresh 0.4 --actions "0.1, 0.2, 0.3, 0.4, 0.5" --alpha 1.0 --gamma 0.1 --tol 1e-6

conda deactivat