#!/bin/bash

# Are you indcluded webcam?

# including, check in /dev/video*
modprobe v4l2loopback devices=2

width=1280
height=720

# translation /dev/video1 /dev/video2
nohup ffmpeg -f video4linux2 -s $(($width))x$(($height)) -i /dev/video0  -codec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/video1  -codec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/video2 >/dev/null 2>/nohup.err &

# params
pause=5
step=1
counter=0

# recording
ffmpeg -y -f v4l2 -framerate 30 -t 5 -video_size $(($width))x$(($height)) -i /dev/video2 -s 640x480 output_0.mkv
