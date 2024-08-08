#!/bin/bash
sinfo --version >> "$(date +"%Y_%m_%d_%I_%M_%p").log"
which sinfo >> "$(date +"%Y_%m_%d_%I_%M_%p").log"
echo $(which sinfo) >> "$(date +"%Y_%m_%d_%I_%M_%p").log"
x=$(which sinfo);
echo $(dirname $x) ;
ls -lrta "$(dirname $x)/../lib/" >> "$(date +"%Y_%m_%d_%I_%M_%p").log"

sbatch --version >> "$(date +"%Y_%m_%d_%I_%M_%p").log"

module purge
module load slurm-drmaa/1.2.0/python2.7
python mod_perform_basecalling.py
