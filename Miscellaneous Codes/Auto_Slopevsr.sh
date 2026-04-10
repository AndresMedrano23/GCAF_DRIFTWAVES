#!/bin/bash
program="Slopevsr.py"
input_folder="ResultadosTRANS/"
output_folder="Imagenes/ResultadosTRANS"


for type in "ra" "nw"; do
    for input_file in "$input_folder"/*.csv; do

        base_name=$(basename "$input_file" .csv)

        output_file="$output_folder/${base_name}_${type}.png"

        echo "Procesando $input_file..."
        python3 "$program" -i "$input_file" -t "$type" -o "$output_file"
    done
done