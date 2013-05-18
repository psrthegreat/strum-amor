var Matrix = require("./Matrix.js");
var MatrixMath = require("./MatrixMath.js");
var BoundNumbers = require("./activationFunction.js").BoundNumbers;

// Construct a BackpropagationLayer that corresponds to a specific neuron layer
BackpropagationLayer = function(backpropagation, layer) {
	this.backpropagation = backpropagation;
	this.layer = layer;

	this.error = new Array(layer.neuronCount);
	this.errorDelta = new Array(layer.neuronCount);

	if (layer.next) {
		this.accMatrixDelta = new Matrix(layer.neuronCount + 1, layer.next.neuronCount);
		this.matrixDelta = new Matrix(layer.neuronCount + 1, layer.next.neuronCount);
		this.biasRow = layer.neuronCount;
	}

	this.calcDelta = function(i) {
		return this.error[i] * this.layer.activationFunction.derivative(this.layer.fire[i]);
	};

	this.clearError = function() {
		for (var i = 0; i < this.layer.neuronCount; i++)
			this.error[i] = 0;
	};

};

BackpropagationLayer.prototype.calcError = function(ideal) {
	var i;
	if (typeof ideal != "undefined") {
		// Calculate layer errors and deltas for the output layer
		for (i = 0; i < this.layer.neuronCount; i++) {
			this.error[i] = BoundNumbers.bound(ideal[i] - this.layer.fire[i]);
			this.errorDelta[i] = BoundNumbers.bound(this.calcDelta(i));
		}
	} else {
		// Calculate the current error
		var next = this.backpropagation.getBackpropagationLayer(this.layer.next);

		for (i = 0; i < this.layer.next.neuronCount; i++) {
			for (var j = 0; j < this.layer.neuronCount; j++) {
				this.accMatrixDelta.add(j, i, next.errorDelta[i] * this.layer.fire[j]);
				this.error[j] = BoundNumbers.bound(this.error[j] + this.layer.matrix.matrix[j][i] * next.errorDelta[i]);
			}
			this.accMatrixDelta.add(this.biasRow, i, next.errorDelta[i]);
		}

		if (this.layer.isHidden()) {
			for (i = 0; i < this.layer.neuronCount; i++)
				this.errorDelta[i] = BoundNumbers.bound(this.calcDelta(i));
		}
	}
};

BackpropagationLayer.prototype.learn = function(learnRate, momentum) {
	if (this.layer.hasMatrix()) {
		var m1 = MatrixMath.multiply(this.accMatrixDelta, learnRate);
		var m2 = MatrixMath.multiply(this.matrixDelta, momentum);
		this.matrixDelta = MatrixMath.add(m1, m2);
		this.layer.setMatrix(MatrixMath.add(this.layer.matrix, this.matrixDelta));
		this.accMatrixDelta.clear();
	}
};

module.exports = BackpropagationLayer;
