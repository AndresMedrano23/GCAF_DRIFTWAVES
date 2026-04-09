#!/bin/bash

pot_type="SUPER"   # puede ser SUPER o RDM
energy=1           # en keV
folder_folder="ResultadosE"


for Amplitude in 0 10e3 10e4 10e5; do
    for num_waves in 1 2 5 10; do
        for r_pos in $(seq 0.2 0.1 0.9); do
           
	    # Generar identificador de archivo
            r_label=$(echo "$r_pos*10" | bc | cut -d'.' -f1)
            basename="A${Amplitude}_R${r_label}_E${energy}_n${num_waves}_${pot_type}"	
	    #hacer carpetas para resultados	    
            mkdir -p "$folder_folder/$basename"
	
            echo "Data, Carpeta y slurm $basename"
        done
    done
done
