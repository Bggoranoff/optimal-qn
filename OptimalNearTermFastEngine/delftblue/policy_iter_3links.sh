#!/bin/bash

#SBATCH --job-name="policy_iter_3links"
#SBATCH --time=15:00:00
#SBATCH --ntasks=1
#SBATCH --partition=compute-p2
#SBATCH --mem-per-cpu=80GB

#SBATCH --cpus-per-task=1
#SBATCH --account=education-eemcs-courses-cse3000
#SBATCH --output=/home/%u/OptimalNearTerm/delftblue/logs/%x_%j.out
#SBATCH --error=/home/%u/OptimalNearTerm/delftblue/logs/%x_%j.err

make clean
make compile
./OptimalNearTerm policyIter 3 0.5 "0.1, 0.2, 0.3, 0.4" 1.0 0.1 1e-20

