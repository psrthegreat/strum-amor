function ErrorCalculation() {

	// Reset the error accumulation to zero.
	this.reset = function() {
		// The current error level
		this.globalError = 0;
		// The size of a training set
		this.setSize = 0;
	};

	// Returns the root mean square error for a complete training set.
	this.calculateRMS = function() {
		return Math.sqrt(this.globalError / this.setSize);
	};

	// Called to update for each number that should be checked. Actual and ideal are number arrays.
	this.updateError = function(actual, ideal) {
		for (var i = 0; i < actual.length; i++) {
			var delta = ideal[i] - actual[i];
			this.globalError += delta * delta;
		}
		this.setSize += ideal.length;
	};

	// Initiate variables.
	this.reset();

}

module.exports = ErrorCalculation;
