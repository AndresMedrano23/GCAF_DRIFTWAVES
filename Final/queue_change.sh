#!/bin/bash
queue_type="icn" #puede ser icn o mpi

for slurms in slurms_L/*;do
	sed -i "10s|.*|#SBATCH --partition=$queue_type # COLA O PARTICION DE EJECUCION|" "$slurms"
done
