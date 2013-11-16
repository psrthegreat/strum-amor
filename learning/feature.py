from cluster import Cluster
import numpy as np

class FeatExtractor(object):
	def __init__(self):
		self.pca = None;
		self.centroids = None;
		self.clustered = False;

	def cluster(self, data, k):
		self.clustered = True;
		self.k = k;
		c = Cluster(data, self.k);
		c.runKMeans();
		self.pca = c.getPCA();
		self.centroids = c.getCentroids();

	def extractSingle(self, data):
		assert self.clustered;
		featureMat = np.empty([data.shape[0], self.k])
		for i in range(data.shape[0]):
			currpatch = pca.transform(data[i, :]).ravel()
			diff = currpatch - centroids
			distances = np.sum(diff ** 2, axis = 1)
			distances = np.sqrt(distances)
			avgDist = np.average(distances)
			for j in range(self.k):
				distanceToJ = distances[j]
				aij = avgDist - distanceToJ
				fij = max(0, aij)
				featureMat[i][j] = fij
		features = featureMat.flatten()
		return features;

	"""where examples comes from d.getLabeled(filename);
	"""
	def extractAll(self, examples):
		assert self.clustered;
		first = True;
		for i in range(len(examples)):
			example = examples[i];
			data = example['data'];
			feats = extractFeatures(data).reshape(1, -1);
			print feats.shape;
			if first:
				X = feats;
				first = False;
			else:
				X = np.append(X, feats, axis = 0);
		return X;
