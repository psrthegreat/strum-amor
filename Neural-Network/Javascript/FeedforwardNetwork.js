var FeedforwardLayer = require("./FeedforwardLayer.js");
var Matrix = require("./Matrix.js");
var MatrixCODEC = require("./MatrixCODEC.js");
var ErrorCalculation = require("./ErrorCalculation.js");

function FeedforwardNetwork() {
	this.layers = [];
	this.hiddenLayerCount = function() {
		return this.layers.length - 2;
	};
	this.matrixSize = function() {
		var matrixSize = 0;
		for (var i = 0; i < this.layers.length; i++)
			matrixSize += this.layers[i].matrixSize();
		return matrixSize;
	};
	this.hiddenLayers = function() {
		var hiddenLayers = [];
		for (var i = 0; i < this.layers.length; i++)
			if (this.layers[i].isHidden())
				hiddenLayers.push(this.layers[i]);
		return hiddenLayers;
	};
}

// Add a layer to the neural network - first layer added is the input layer, last layer added is the output.
FeedforwardNetwork.prototype.addLayer = function(layer) {
	// Set up 'previous' in the new layer and 'next' in the last layer
	if (this.outputLayer) {
		layer.previous = this.outputLayer;
		this.outputLayer.next = layer;
		this.outputLayer.matrix = new Matrix(this.outputLayer.neuronCount + 1, layer.neuronCount);
	}

	// Update the inputLayer and outputLayer variables
	if (this.layers.length === 0) {
		this.inputLayer = this.outputLayer = layer;
	} else {
		this.outputLayer = layer;
	}

	// Add the new layer to the layers list
	this.layers.push(layer);
};

// Calculate the root mean square error for this neural network. Input and ideal are 2D arrays
FeedforwardNetwork.prototype.calcError = function(input, ideal) {
	var errorCalculation = new ErrorCalculation();

	for (var i = 0; i < ideal.length; i++) {
		this.computeOutputs(input[i]);
		errorCalculation.updateError(this.outputLayer.fire, ideal[i]);
	}

	return errorCalculation.calculateRMS();
};

// Calculate the total number of neurons in the network across all layers.
FeedforwardNetwork.prototype.calculateNeuronCount = function() {
	var count = 0;
	for (var i = 0; i < this.layers.length; i++)
		count += this.layers[i].neuronCount;
	return count;
};

// Create a clone of the neural network.
FeedforwardNetwork.prototype.clone = function() {
	var clone = this.cloneStructure();
	var copy = MatrixCODEC.networkToArray(this);
	MatrixCODEC.arrayToNetwork(copy, clone);
	return clone;
};

// Create a clone of the structure of the neural network.
FeedforwardNetwork.prototype.cloneStructure = function() {
	var clone = new FeedforwardNetwork();
	for (var i = 0; i < this.layers.length; i++) {
		var layerClone = new FeedforwardLayer(this.layers[i].neuronCount);
		clone.addLayer(layerClone);
	}
	return clone;
};

// Compute the output for a given input to the neural network.
FeedforwardNetwork.prototype.computeOutputs = function(input) {
	if (input.length != this.inputLayer.neuronCount) throw new Error("Input size must match input layer size");

	for (var i = 0; i < this.layers.length; i++) {
		if (this.layers[i].isInput())
			this.layers[i].computeOutputs(input);
		else if (this.layers[i].isHidden())
			this.layers[i].computeOutputs();
	}

	return this.outputLayer.fire;
};

// Compare two neural netowrks.
FeedforwardNetwork.prototype.equals = function(other) {
	for (var i = 0; i < this.layers.length; i++) {
		var layer = this.layers[i];
		var otherLayer = other.layers[i];
		if (layer.neuronCount != otherLayer.neuronCount) return false;
		
		// Both layers must either have or not have a weight matrix
		if (!layer.matrix && otherLayer.matrix) return false;
		if (layer.matrix && !layer.matrix) return false;
		
		// If they both have a matrix, compare the matrices
		if (layer.matrix && otherLayer.matrix)
			if (!layer.matrix.equals(otherLayer.matrix))
				return false;
	}

	return true;
};

// Reset the weight matrix and the thresholds.
FeedforwardNetwork.prototype.reset = function() {
	for (var i = 0; i < this.layers.length; i++)
		this.layers[i].reset();
};

module.exports = FeedforwardNetwork;
