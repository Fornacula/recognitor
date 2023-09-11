#!/bin/bash

# Make dir for cropped images
# Define the directory path
directory_path="./cropped"

# Check if the directory exists
if [ ! -d "$directory_path" ]; then
    # Create the directory
    mkdir -p "$directory_path"
    echo "Directory '$directory_path' created."
else
    echo "Directory '$directory_path' already exists."
fi


# Check if ImageMagick (convert) is installed
if ! command -v convert &> /dev/null; then
    echo "ImageMagick (convert) is not installed. Please install it."
    exit 1
fi

# Input image file
input_image="image.jpg"

size_x=555
size_y=28
position_x=45
position_y=13

# Crop the image 16 times (16 rows)
for ((i=1; i<=16; i++)); do
  echo "Cropping row $i into $directory_path/row_$i.jpg..."
  convert "$input_image" -crop "$size_x"x"$size_y"+"$position_x"+"$((i * size_y + position_y))" "$directory_path/row_$i.jpg"
done
