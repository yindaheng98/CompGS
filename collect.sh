#!/bin/bash
mkdir -p CompGS
root=results/Videos
for video in $(ls $root); do
folder=$root/$video/frame1/Lambda0_001
    for datetime in $(ls $folder); do
        file=$folder/$datetime/eval/results.json
        echo "Processing $file"
        if [ ! -f $file ]; then
            echo "File $file does not exist, skipping."
            continue
        fi
        cp $file CompGS/$video.json
        break
    done
done