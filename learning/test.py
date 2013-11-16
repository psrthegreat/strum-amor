from cluster import Cluster
from datagen import DataGen
import numpy as np
k = 5 
c = Cluster(k);
c.runKmeans();
pca = c.getPCA();
centroids = c.getCentroids();

def extractFeatures(data):
	featureMat = np.empty([data.shape[0], k])
	for i in range(data.shape[0]):
		currpatch = pca.transform(data[i, :]).ravel()
		diff = currpatch - centroids
		distances = np.sum(diff ** 2, axis = 1)
		distances = np.sqrt(distances)
		avgDist = np.average(distances)
		for j in range(k):
			distanceToJ = distances[j]
			aij = avgDist - distanceToJ
			fij = max(0, aij)
			featureMat[i][j] = fij
	features = featureMat.flatten()
	return features;

d = DataGen('./csvs/');
examples =  d.getLabeled('list');
for example in examples:
	label = example['label'];
	data = example['data'];
	feats = extractFeatures(data);
	print feats

c.visualize();
