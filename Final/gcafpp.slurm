#!/bin/bash
#SBATCH --job-name=FTLE   # NOMBRE DEL JOB
#SBATCH --nodes=1              # CANTIDAD DE NODOS SOLICITADOS
#SBATCH --tasks=1              # CANTIDAD DE PROCESOS SIMULTANEOS
#SBATCH --cpus-per-task=8      # CORES POR PROCESO
#SBATCH --mem=20MB             # MEMORIA SOLICITADA
#SBATCH --time=96:00:00        # TIEMPO MAXIMO DE EJECUCION
#SBATCH --output=out.log       # ARCHIVO PARA LA SALIDA ESTANDAR
#SBATCH --error=err.log        # ARCHIVO PARA MENSAJES DE ERROR
#SBATCH --partition=mpi        # COLA O PARTICION DE EJECUCION

module purge
module load lamod/gcc/4.9
module load lamod/boost/1.80
module load lamod/openmpi/4.1

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

echo "Running on host " $(hostname)
echo "Time is " $(date)
echo "Processors used: $SLURM_NODELIST"
#    1 nodos X 8 tasks por nodo = 8 cores
srun gcafpp -i data.in -t lyap -o ResultadosL/Prueba -d tkmk  

echo "Done"

