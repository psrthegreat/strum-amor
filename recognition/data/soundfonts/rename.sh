for file in ./*
do
	filename=${file##*/}
	mv "$file" "./Scc1t2_$filename"
done
