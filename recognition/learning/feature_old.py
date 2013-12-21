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
		#c.visualize();
		self.pca = c.getPCA();
		self.centroids = c.getCentroids();

	def extractSingle(self, data):
		assert self.clustered;
		featureMat = np.empty([data.shape[0], self.k])
		for i in range(data.shape[0]):
			currpatch = self.pca.transform(data[i, :]).ravel()
			diff = currpatch - self.centroids
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
			feats = self.extractSingle(example).reshape(1, -1);
			if first:
				X = feats;
				first = False;
			else:
				X = np.append(X, feats, axis = 0);
		return X;
