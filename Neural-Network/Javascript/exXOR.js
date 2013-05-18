var FeedforwardNetwork = require("./FeedforwardNetwork.js");
var FeedforwardLayer = require("./FeedforwardLayer.js");
var Backpropagation = require("./Backpropagation.js");
var SimulatedAnnealing = require("./SimulatedAnnealing.js");
var GeneticAlgorithm = require("./GeneticAlgorithm.js");

// Input for the XOR function
var input = [[0, 0], [1, 0], [0, 1], [1, 1]];
// Ideal output for the XOR function
var ideal = [[0], [1], [1], [0]];

// Create the feedforward network
var network = new FeedforwardNetwork();
network.addLayer(new FeedforwardLayer(2));
network.addLayer(new FeedforwardLayer(3));
network.addLayer(new FeedforwardLayer(1));
network.reset();

// Train the neural network
var train = new Backpropagation(network, input, ideal, 0.7, 0.9);
//var train = new SimulatedAnnealing(network, input, ideal, 10, 2, 100);
//var train = new GeneticAlgorithm(network, input, ideal, true, 5000, 0.1, 0.25);

var epoch = 1;
do {
	train.iteration();
	console.log("Epoch #"+epoch+" Error: "+train.error);
	epoch++;
} while (epoch < 1000 && train.error > 0.001);

// Test the neural network
console.log("Neural Network Results:");
for (var i = 0; i < ideal.length; i++) {
	var actual = network.computeOutputs(input[i]);
	console.log(input[i]+" Actual: "+actual[0]+" Ideal: "+ideal[i][0]);
}
