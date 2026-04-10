#!/bin/bash
program="trajectory_plot.py"

for input_folder in "ResultadosT/Long"/*; do
    folder_name=$(basename "$input_folder")
    output_folder="Imagenes/ResultadosT/Deuterium/Long/${folder_name}"
    for type in "rvsz" "3d"; do
        for file in $input_folder/*.plt; do
            echo "Processing $file..."
            filename=$(basename "$file" .plt)
            output_file="$output_folder/${filename}_${type}.png"
            python3 "$program" -i "$file" -t "$type" -o "$output_file"
        done
    done
done