#! /bin/bash

##
## Generates a video in order to verify visually
## the animation generated
##

rm -f monit_anim.avi
ffmpeg -i ../data/monitor/%d.bmp -r 25 monit_anim.avi 
vlc monit_anim.avi &&
rm monit_anim.avi
