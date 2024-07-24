#!/bin/bash

# 图片文件列表
image_files=("图片1.png" "图片2.png" "图片9.png" "图片10.png")

# 目标大小
target_size="256x256"

# 遍历所有图片文件并调整大小
for image_file in "${image_files[@]}"
do
    convert "$image_file" -resize "$target_size" "resized_$image_file"
done

echo "All images have been resized."

