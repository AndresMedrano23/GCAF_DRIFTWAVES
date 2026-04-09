#!/bin/bash
## Automaticamente recorre todos las carpetas dentro de un folder especificado
# si solo queremos un folder basta con darle la ruta comple
program="distribution_plot2.py"
type="pos"
#base_input="ResultadosE/TEMP_70"
#base_output="Imagenes/ResultadosE/TEMP_70"
filename="dist_"

# Recorre todas las carpetas dentro de ResultadosE
for base_input in  "ResultadosE/SECH_ISO" ; do
    base_output="Imagenes/$base_input"
    for folder in "$base_input"/*/; do
        # Nombre de la carpeta sin la ruta base
        subfolder=$(basename "$folder")
        input_folder="$base_input/$subfolder"
        output_folder="$base_output/$subfolder"

        echo "Procesando carpeta: $subfolder"

        # Ejecutar moments_plot.py
        python3 Ancho_plot.py -i "$input_folder/mome.plt" -o "$output_folder/mome1.png"

        #Loop para distribution_plot.py
        for i in $(seq 0 25 1); do
            input_file="$input_folder/${filename}$i.plt"
            output_file="$output_folder/${filename}$i.png"
            python3 "$program" -i "$input_file" -t "$type" -o "$output_file"
        done
    done
done