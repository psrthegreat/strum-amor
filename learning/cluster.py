import numpy as np
import pylab as pl
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

class Cluster(object):
	def __init__(self, data, k):
		self.kmeans = None;
		self.numCategories = k;
		self.data = data;
		self.n_samples, self.n_features = data.shape;
		self.trained = False;
		self.reduced_data = None;
		self.pca = None;

	def getCentroids(self):
		assert self.trained;
		return self.kmeans.cluster_centers_;

	def getPCA(self):
		assert self.trained;
		return self.pca;

	def runKMeans(self):
		self.pca = PCA(n_components=2);
		self.pca.fit(self.data);
		self.reduced_data =self.pca.fit_transform(self.data)
		self.kmeans = KMeans(init='k-means++', n_clusters=self.numCategories, n_init=10)
		self.kmeans.fit(self.reduced_data)
		self.trained = True;

	def visualize(self):
		assert self.trained;
		# Step size of the mesh. Decrease to increase the quality of the VQ.
		h = .02     # point in the mesh [x_min, m_max]x[y_min, y_max].

		# Plot the decision boundary. For that, we will assign a color to each
		x_min, x_max = self.reduced_data[:, 0].min() + 1, self.reduced_data[:, 0].max() - 1
		y_min, y_max = self.reduced_data[:, 1].min() + 1, self.reduced_data[:, 1].max() - 1
		xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

		# Obtain labels for each point in mesh. Use last trained model.
		Z = self.kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
		# Put the result into a color plot
		Z = Z.reshape(xx.shape)
		pl.figure(1)
		pl.clf()
		pl.imshow(Z, interpolation='nearest',
				extent=(xx.min(), xx.max(), yy.min(), yy.max()),
				cmap=pl.cm.Paired,
				aspect='auto', origin='lower')
		#plotting the data points themselves
		pl.plot(self.reduced_data[:, 0], self.reduced_data[:, 1], 'k.', markersize=2)
		# Plot the centroids as a white X
		centroids = self.kmeans.cluster_centers_
		pl.scatter(centroids[:, 0], centroids[:, 1],
				marker='x', s=169, linewidths=3,
				color='w', zorder=10)
		pl.title('K-means clustering (PCA-reduced data)\n'
				'Centroids are marked with white cross')
		pl.xlim(x_min, x_max)
		pl.ylim(y_min, y_max)
		pl.xticks(())
		pl.yticks(())
		pl.show()
