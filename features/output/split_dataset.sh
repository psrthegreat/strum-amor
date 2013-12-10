#!/bin/bash

split() {
	# filter files with grep
	grep=$(ls $1 | grep -P $2)
	# split files into test and train groups
	n=$(echo "$grep" | wc -l)
	ntest=$((n * 3/10))
	ntrain=$((n - ntest))
	# shuffle files and append to list
	ftest="${1}test"
	ftrain="${1}train"
	# echo "$grep" | shuf | tee >(head -$ntest >> $ftest) | tail -$ntrain >> $ftrain
}

generate_lists() {
	ftest="${1}test"
	ftrain="${1}train"
	if [ -f $ftest ]; then
		rm "$ftest"
	fi
	if [ -f $ftrain ]; then
		rm "$ftrain"
	fi
	touch $ftest
	touch $ftrain

	# split for each key
	keys="C Csh D Dsh E F Fsh G Gsh A Ash B"
	for key in $keys; do
		split $1 "${key}[0-9]"
	done

	# shuffle lists at the end
	cat $ftest | shuf > $ftest
	cat $ftrain | shuf > $ftrain
}

if [[ -z $1 ]]; then
	for instr in */; do
		for dir in $instr*/; do
			generate_lists $dir
		done
	done
fi

for arg; do
	generate_lists $arg
done


# echo $files | head
# mkdir "${1}wav"
# # file=midi_files/maj4C0.mid
# # bool=false
# for sfile in midi_files/soundfonts/*.sf2
# do
#     # if [[ $sfile = "midi_files/soundfonts/Scc1t2_Square.sf2" ]]; then
#     #     bool=true
#     # fi

#     # echo $sfile
#     # if [[ $bool = "false" ]]; then
#     #     continue
#     # fi
#     dir=${1}wav/${sfile##*/}
#     dir=${dir%.*}
#     mkdir "$dir"
#     touch "${dir}/files.txt"
#     for file in $1*.mid
#     do
#         ofile=${file/%mid/wav}
#         ofile=${ofile##*/}
#         FluidSynth/fluidsynth -F "${dir}/${ofile}" -i -n -T wav "$sfile" "$file"
#         # echo $sfile
#         # FluidSynth/fluidsynth -i -n "$sfile" "$file"
#         echo "$ofile" >> "${dir}/files.txt"
#     done
# done
