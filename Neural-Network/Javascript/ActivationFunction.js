/*
 * USE:
 *
 * var activation = new Activation.Linear();
 * activation.fx(.500);
 * activation.derivative(.500);
*/

// Activation functions class
function Activation() {}

// y = x
// dy/dx = 1
// D:(-∞,∞) R:(-∞,∞)
Activation.Linear = function() {
	this.fx = function(value) {
		return value;
	};
	this.derivative = function(value) {
		return 1;
	};
};

// y = 1 / (1 + e^-x)
// dy/dx = y * (1 - y)
// D:(-∞,∞) R:(0,1)
Activation.Sigmoid = function() {
	this.fx = function(value) {
		return 1 / (1 + BoundNumbers.exp(-1 * value));
	};
	this.derivative = function(value) {
		return value * (1 - value);
	};
};

// y = (e^2x - 1) / (e^2x + 1)
// dy/dx = 1 - y^2
// D:(-∞,∞) R:(-1,1)
Activation.TanH = function() {
	this.fx = function(value) {
		return (BoundNumers.exp(2 * value) - 1) / (BoundNumbers.exp(2 * value) + 1);
	};
	this.derivative = function(value) {
		return 1 - Math.pow((BoundNumers.exp(2 * value) - 1) / (BoundNumbers.exp(2 * value) + 1), 2);
	};
};

function BoundNumbers() {}

// Restrict numbers between a lower and upper bound
BoundNumbers.bound = function(value) {
	var lower = -1.0 * Math.pow(10, 20);
	var upper = 1.0 * Math.pow(10, 20);
	if (value < lower) return lower;
	else if (value > upper) return upper;
	else return value;
};

// Return e^x within the bound
BoundNumbers.exp = function(value) {
	return BoundNumbers.bound(Math.exp(value));
};

exports.Activation = Activation;
exports.BoundNumbers = BoundNumbers;
