#!/bin/bash
#PBS -q beta
#PBS -l select=1:ncpus=24:mpiprocs=24
#PBS -l walltime=60:00:00
#PBS -N autres_job
#PBS -j oe
#PBS -M ljudmila.petkovic@sorbonne-universite.fr
#PBS -m bae

## Use multiple of 2 with a maximum of 24 on 'ncpus' parameter, one node has 24 cores max
## With the 'select=3:ncpus=10:mpiprocs=10' option you get 30 cores on 3 nodes
## If you use select=1:ncpus=30 your job will NEVER run because no node has 30 cores.

# load modules
#. /etc/profile.d/modules.sh
 
#load appropriate modules
# module purge
# module load intel-compilers-18.0/18.0
# module load mpt/2.18
module load python/3.10

#move to PBS_O_WORKDIR
cd $PBS_O_WORKDIR
 
# Define scratch space scratchbeta on ICE XA
SCRATCH=/scratchbeta/$USER
PROJECT='projet_charcot'
#mkdir $SCRATCH
mkdir -p "$SCRATCH/$PROJECT"

rm -rf "$SCRATCH/output"
mkdir -p "$SCRATCH/output"

# copy some input files to  $SCRATCH directory
rm -rf /scratchbeta/petkovic/corpus
cp -r corpus /scratchbeta/petkovic/

#execute your program
## With SGI MPT use 'mpiexec_mpt -np 30 myprogram' to use mpt correctly for example

cp keyphrase-vectorizers.py /scratchbeta/petkovic/$PROJECT

cd $SCRATCH/$PROJECT || exit 1
python3 ./keyphrase-vectorizers.py

# copy some output files to submittion directory and delete temporary work files
# cp -p /scratchbeta/petkovic/output/autres_keyphv.txt $PBS_O_WORKDIR || exit 1
 
#clean the temporary directory
# rm -rf "$SCRATCH/$PROJECT"/*
