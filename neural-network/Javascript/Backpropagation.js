require("./BackpropagationLayer.js");

// network: FeedforwardNetwork to be trained
// input: 2D array of input values to the neural network
// ideal: 2D array of ideal values expected from the neural network
// learnRate: double specifying how fast to modify neural network values
// momentum: double specifying how much to use the previous training iteration for the next
Backpropagation = function(network, input, ideal, learnRate, momentum) {
	this.network = network;
	this.learnRate = learnRate;
	this.momentum = momentum;
	this.input = input;
	this.ideal = ideal;

	// layer map
	this.layers = new Array(this.network.layers.length);
	for (var i = 0; i < network.layers.length; i++) {
		this.layers[i] = new BackpropagationLayer(this, network.layers[i]);
	}
};

// Calculate the error for the output yield
Backpropagation.prototype.calcError = function(ideal) {
	if (ideal.length != this.network.outputLayer.neuronCount)
		throw new Error("Ideal input size and output layer size don't match.");
	
	// Clear out all previous error data
	for (var i = 0; i < this.network.layers.length; i++)
		this.getBackpropagationLayer(this.network.layers[i]).clearError();

	for (i = this.network.layers.length - 1; i >= 0; i--) {
		var layer = this.network.layers[i];
		if (layer.isOutput()) {
			this.getBackpropagationLayer(layer).calcError(ideal);
		} else {
			this.getBackpropagationLayer(layer).calcError();
		}
	}
};

// Get the backpropagation layer that corresponds to the specified layer
Backpropagation.prototype.getBackpropagationLayer = function(layer) {
	return this.layers[this.network.layers.indexOf(layer)];
};

// Perform one iteration of training
Backpropagation.prototype.iteration = function() {
	for (var i = 0; i < this.input.length; i++) {
		this.network.computeOutputs(this.input[i]);
		this.calcError(this.ideal[i]);
	}
	this.learn();

	this.error = this.network.calcError(this.input, this.ideal);
};

// Modfiy the weight matrix and thresholds based on the last call to calcError
Backpropagation.prototype.learn = function() {
	for (var i = 0; i < this.network.layers.length; i++)
		this.getBackpropagationLayer(this.network.layers[i]).learn(this.learnRate, this.momentum);
};

module.exports = Backpropagation;
