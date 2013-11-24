var Matrix = require("./Matrix.js");
var MatrixMath = require("./MatrixMath.js");
var Activation = require("./activationFunction.js").Activation;

// Construct a feedforward layer with the specified number of neurons and an optional threshold function.
function FeedforwardLayer(neuronCount, thresholdFunction) {
	if (typeof neuronCount != "number") throw new Error("neuronCount must be an integer");
	this.fire = new Array(neuronCount);
	this.neuronCount = neuronCount;
	this.activationFunction = arguments.length == 2 ? thresholdFunction : new Activation.Sigmoid();

	this.matrixSize = function() {
		if (!this.matrix) return 0;
		else return this.matrix.size();
	};
	this.hasMatrix = function() {
		return (!!this.matrix);
	};
	this.isHidden = function() {
		return (this.next && this.previous);
	};
	this.isInput = function() {
		return (!this.previous);
	};
	this.isOutput = function() {
		return (!this.next);
	};
}

FeedforwardLayer.prototype.setMatrix = function(matrix) {
	if (matrix.rows < 2) throw new Error("Weight matrix includes threshold values and must have at least 2 rows.");
	if (matrix) this.fire = new Array(matrix.rows - 1);
	this.matrix = matrix;
};

// Clone the structure of this layer, but not the matrix data
FeedforwardLayer.prototype.cloneStructure = function() {
	return new FeedforwardLayer(this.activationFunction, this.neuronCount);
};

// Compute the outputs for this layer given the input pattern. The output is stored in the fire instance.
FeedforwardLayer.prototype.computeOutputs = function(pattern) {
	var i;
	if (typeof pattern != "undefined") {
		for (i = 0; i < this.neuronCount; i++)
			this.fire[i] = pattern[i];
	}

	var inputMatrix = FeedforwardLayer.createInputMatrix(this.fire);

	for (i = 0; i < this.next.neuronCount; i++) {
		var col = this.matrix.getCol(i);
		var sum = MatrixMath.dotProduct(col, inputMatrix);
		this.next.fire[i] = this.activationFunction.fx(sum);
	}
	return this.fire;
};

// Turn a double array into a matrix that can be used calculate the results of the input array with the threshold.
FeedforwardLayer.createInputMatrix = function(pattern) {
	var input = new Matrix(1, pattern.length + 1);
	for (var i = 0; i < pattern.length; i++) {
		input.matrix[0][i] = pattern[i];
	}
		

	// Add a fake first column to the input so that the threshold is always multiplied by one, result in it just being added.
	input.matrix[0][pattern.length] = 1;

	return input;
};

FeedforwardLayer.prototype.setNext = function(value) {
	this.next = value;

	// Add one to the neuron count to provide a threshold value in row 0
	this.matrix = new Matrix(this.neuronCount + 1, this.next.neuronCount);
};

// Prune the specified neuron from this layer. Remove all entries in this weight matrix and other layers.
FeedforwardLayer.prototype.prune = function(neuron) {
	// Delete a row from this matrix
	if (this.matrix)
		this.setLayerMatrix(MatrixMath.deleteRow(this.matrix, neuron));

	// Delete a column from the previous layer
	if (this.previous && this.previous.matrix)
		this.previous.setLayerMatrix(MatrixMath.deleteCol(this.previous.matrix, neuron));
};

// Reset the weight matrix and threshold values to random numbers between -1 and 1.
FeedforwardLayer.prototype.reset = function() {
	if (this.matrix) this.matrix.randomize(-1, 1);
};

module.exports = FeedforwardLayer;
