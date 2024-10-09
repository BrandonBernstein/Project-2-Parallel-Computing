#!/bin/bash

#SBATCH --job-name=reduce_problem
#SBATCH --output=time_taken_1.out
#SBATCH --ntasks-per-node=16
#SBATCH --nodes=1
#SBATCH --time=02:00
#SBATCH -p short-40core
#SBATCH --mail-type=END
#SBATCH --mail-user=brandon.bernstein@stonybrook.edu

module load mvapich2/gcc12.1/2.3.7

mpiexec -n 16 python main.py
