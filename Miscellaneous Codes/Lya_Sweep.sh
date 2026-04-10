#!/bin/bash

base_input="ResultadosL/SECH_PT20"
#When we have an already precomputed file just need to plot
program="FTLE_Convergence.py"
for dist_type in "tor" "cart"; do
    for folder in "$base_input"/*/; do
        echo "Procesando carpeta: $folder"
        folder_name=$(basename "$folder")
        file_name="${folder}/lyapunov_average_${dist_type}.dat"
        python3 "$program" -i $file_name -logsep -o "${base_input}/${folder_name}/${dist_type}"
    done
done
