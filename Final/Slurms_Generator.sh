#!/bin/bash

pot_type="SUPER"   # puede ser SUPER o RDM
energy=1           # en keV
output_folder="slurms"
queue = "icn"  #mpi o icn


      # COLA O PARTICION DE EJECUCION
sed -i "10s/.*/#SBATCH --partition= $queue/" "$output_folder/$filename
