#!/bin/bash

# Slurm job options (job-name, compute nodes, job time)
#SBATCH --job-name=convection_test
#SBATCH --time=14:20:0
#SBATCH --nodes=20
#SBATCH --tasks-per-node=128
#SBATCH --cpus-per-task=1

# Replace [budget code] below with your budget code (e.g. t01)
#SBATCH --account=e723-kevinb
#SBATCH --partition=standard
#SBATCH --qos=standard

# Setup the job environment (this module needs to be loaded before any other modules)
#  module load epcc-job-env

# Set the number of threads to 1
#   This prevents any threaded system libraries from automatically 
#   using threading.

module list
# module load load-epcc-module
# module load epcc-setup-env
# export CRAY_ADD_RPATH=yes
# module swap PrgEnv-cray PrgEnv-gnu
# module load cray-fftw
# module load cmake


export OMP_NUM_THREADS=1

export FI_MR_CACHE_MAX_COUNT=0

export PATH="/mnt/lustre/a2fs-work2/work/e723/e723/kevinb/miniconda3/bin:$PATH"
# conda activate py38

export PATH="/mnt/lustre/a2fs-work2/work/e723/e723/kevinb/.local/.local/bin:$PATH"

export NEK_DIR=/mnt/lustre/a2fs-work2/work/e723/e723/kevinb/nektarpp/build
export NEK_BUILD=$NEK_DIR/dist/bin
export LD_LIBRARY_PATH=/opt/gcc/10.2.0/snos/lib64:$NEK_DIR/ThirdParty/dist/lib:$NEK_DIR/dist/lib64:$LD_LIBRARY_PATH
export PATH="/mnt/lustre/a2fs-work2/work/e723/e723/kevinb/nektarpp/build/dist/bin:$PATH"

# Launch the parallel job
start_time="$(date -u +%s.%n)"



echo "starting convection 3D!"

srun --distribution=block:block --hint=nomultithread IncNavierStokesSolver convection_3d.xml  convection_3d_mesh.xml --npz 4 -i Hdf5 &> runlog

end_time="$(date -u +%s.%n)"
elapsed="$(bc <<<"$end_time-$start_time")"
echo -e "\n\nTotal Executing Time = $elapsed seconds\n" > time.txt

