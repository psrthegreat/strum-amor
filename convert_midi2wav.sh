#!/bin/bash

mkdir ${1}wav
for sfile in midi_files/soundfiles/*.sf2
do
	dir=${1}wav/${sfile##*/}
	dir=${dir%.*}
	mkdir $dir
	for file in $1*.mid
	do
		ofile=${file/%mid/wav}
		ofile=${dir}/${ofile##*/}
		FluidSynth/fluidsynth.exe -F "$ofile" -i -n "$sfile" "$file"
	done
done