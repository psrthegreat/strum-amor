from datagen import DataGen

dgen = DataGen();
data = dgen.readCsvs('./csvs/', 'list');
print data.shape
