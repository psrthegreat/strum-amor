yaafe.py -c featureplan -r 44100 -i ../../strum-amor-data/wav -o csv -p Metadata=False
datadir=../../strum-amor-data/
for instrdir in ${datadir}wav/*/
do
	instr=${instrdir%.*}
	echo "yaafe.py -c featureplan -r 44100 -i ${instrdir}files.txt -b ${datadir}csv/${datadir} -o csv -p Metadata=False"
done
