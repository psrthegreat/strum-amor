#implements the training pipeline
from sklearn.preprocessing import scale
from feature import FeatExtractor
from datagen import DataGen

def loadData(path, filename):
	dgen = DataGen(path);
	data = dgen.getUnlabeled(filename);
	data = scale(data);
	return data;

data = loadData('./csvs/', 'list');
k = 10
fe = FeatExtractor();
fe.cluster(data, 10);
