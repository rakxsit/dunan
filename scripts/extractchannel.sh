#!/bin/bash

# Usage: bash extractchannel.sh folder channel
# Extract only left or right channel (left = 1, right = 2)

dir=$1
channel=$2

mkdir "$dir""-mono"
for file in "$dir"/*.wav; 
do
	fname=$(basename $file .wav)
	sox $file $dir"-mono"/$fname'.wav' remix $channel
done