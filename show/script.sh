#!/bin/bash

# 输入视频文件
input_file="媒体2.mp4"

# 提取最后一帧
ffmpeg -sseof -1 -i "$input_file" -update 1 -q:v 1 last_frame.jpg

# 创建一个持续5秒的最后一帧视频
ffmpeg -loop 1 -i last_frame.jpg -c:v libx264 -t 5 -pix_fmt yuv420p last_frame.mp4

# 合并原视频和延长的最后一帧视频
#ffmpeg -i "$input_file" -i last_frame.mp4 -filter_complex "[0:v][1:v]concat=n=2:v=1[outv]" -map "[outv]" -map 0:a? -c:a copy v1.mp4

