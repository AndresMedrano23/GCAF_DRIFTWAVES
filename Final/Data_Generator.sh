#!/bin/bash

pot_type="RDM"   # puede ser SUPER o RDM
energy=1           # en keV
data_folder="data_inputs_L"
slurm_folder="slurms_L"
folder_folder="ResultadosE/Long/SECH_PT70_RDM"
queue_type="mpi" # puede ser mpi o icn
pt_type="fix"
sim_type="ense" #ense lyap traj poin

sed -i "10s|.*|#SBATCH --partition=$queue_type        # COLA O PARTICION DE EJECUCION|" "gcafpp.slurm"

for pitch in 70; do
    #for Amplitude in 0 10e4; do
    for Amplitude in 0 10e3 10e4 10e5 10e6; do
        for num_waves in 1 2 5 10 20 ; do
            for r_pos in $(seq 0.2 0.1 0.9); do
            #for r_pos in 0.2; do
            # Generar identificador de archivo
                r_label=$(echo "$r_pos*10" | bc | cut -d'.' -f1)
                basename="A${Amplitude}_R${r_label}_E${energy}_n${num_waves}_PT${pitch}_${pt_type}_${pot_type}"
            
                # Copiar plantilla original de data.in  y modificar
           	#IMPORTANTE todo lo demás ya debe estar adecuado.
                cp data.in "$data_folder/${basename}.in"

                # Sustituir líneas del data in
                sed -i "23s/.*/electrostatic_potential = $pot_type $Amplitude $num_waves/" "$data_folder/${basename}.in"
                sed -i "41s/.*/radial_position         = $r_pos/" "$data_folder/${basename}.in"
                sed -i "44s/.*/pitch_angle             = $pt_type $pitch/" "$data_folder/${basename}.in"
                sed -i "45s/.*/energy                  = mono $energy/" "$data_folder/${basename}.in"
        
            #Ahora para los Slurms
            cp gcafpp.slurm "$slurm_folder/${basename}.slurm"
            
            #Sustituir slurm
            #Identificador de job
            #sed -i "2s|.*|#SBATCH --job-name=$Amplitude $num_waves $r_label $pot_type  # NOMBRE DEL JOB|" "$slurm_folder/${basename}.slurm"	
            	sed -i "23s|.*|srun gcafpp -i $data_folder/${basename}.in -t $sim_type -o $folder_folder/${basename} -d tkmk|" "$slurm_folder/${basename}.slurm"	
            #hacer carpetas para resultados	    
            	mkdir -p "$folder_folder/$basename"
        
                echo "Data, Carpeta y slurm $basename"
            done
        done
    done
done
