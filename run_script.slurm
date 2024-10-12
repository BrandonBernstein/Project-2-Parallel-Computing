#!/bin/bash
#
#SBATCH --job-name=proj2
#SBATCH --output=out2_specific_2.txt
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --time=1:00:00
#SBATCH --partition=short-96core

module load gcc/12.1.0
module load mpi4py/3.0.3

mpirun python /gpfs/home/bsbernstein/main_1e8.py
