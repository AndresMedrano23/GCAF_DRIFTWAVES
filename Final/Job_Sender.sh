#!/bin/bash

slurm_folder="slurms_L"  # la carpeta donde están tus .slurm

# Recorrer todos los archivos .slurm y enviarlos a la cola
for slurm_file in "$slurm_folder"/*.slurm; do
    if [ -f "$slurm_file" ]; then #solo archivos
        echo "Enviando $slurm_file a la cola..."
        sbatch "$slurm_file"
    fi
done

echo "Todos los trabajos han sido enviados."
