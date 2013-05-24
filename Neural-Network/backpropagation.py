"""Backpropagation training class for feedforward networks"""

import numpy

class Backpropagation:
    """Backpropagation interface"""
    def __init__(self, network, input, ideal, learnRate, momentum):
        self.network = network      # reference to parent network
        self.input = input          # array of inputs
        self.ideal = ideal          # array of ideal outputs
        self.learnRate = learnRate  # speed of learning (0.0-1.0)
        self.momentum = momentum    # influence of previous generations (0.0-1.0)
        self.error = None           # error of current generation

        # array of backpropagation layers corresponding to network layers
        self.layers = [BackpropagationLayer(self, layer) for layer in network.layers]
        for layer in self.layers[:-1]:
            layer.connectNext()

    def calcError(self, ideal):
        """Calculate error for output yield"""
        for layer in self.layers:
            layer.clearError()

        for i in range(len(self.network.layers) - 1, -1, -1):
            if self.network.layers[i].isOutput():
                self.layers[i].calcError(ideal)
            else:
                self.layers[i].calcError()

    def iteration(self):
        """Perform one iteration of training"""
        for i in range(len(self.input)):
            self.network.computeOutputs(self.input[i])
            self.calcError(self.ideal[i])
        self.learn()

        self.error = self.network.calcError(self.input, self.ideal)

    def learn(self):
        """Modify weight matrix based on last call to calcError"""
        for layer in self.layers:
            layer.learn(self.learnRate, self.momentum)

class BackpropagationLayer:
    """Backpropagation layer corresponding to neuron layer"""
    def __init__(self, backpropagation, layer):
        self.backpropagation = backpropagation  # reference to backpropagation parent
        self.layer = layer                      # reference to corresponding network layer
        self.next = None                        # next backpropagation layer
        self.error = numpy.zeros(layer.neuronCount)         # error for each neuron
        self.errorDelta = numpy.zeros(layer.neuronCount)    # errorDelta for each neuron

        if not layer.isOutput():
            self.accMatrixDelta = numpy.zeros((layer.neuronCount + 1, layer.next.neuronCount))
            self.matrixDelta = numpy.zeros((layer.neuronCount + 1, layer.next.neuronCount))
            self.biasRow = layer.neuronCount    # index of bias in weight matrix

    def connectNext(self):
        """Connect this layer to next one"""
        layers = self.backpropagation.layers
        self.next = layers[layers.index(self) + 1]

    def calcDelta(self):
        """Error delta"""
        return [self.layer.activationFunction.df(neuron) for neuron in self.layer.neurons]

    def clearError(self):
        """Clear error after every generation"""
        self.error[:] = 0

    def calcError(self, ideal = None):
        """Calculate error for this layer"""
        if ideal is not None:
            self.error = ideal - self.layer.neurons
            self.errorDelta = self.error * self.calcDelta()
        else:
            for i in range(self.layer.next.neuronCount):
                for j in range(self.layer.neuronCount):
                    self.accMatrixDelta[j][i] += self.next.errorDelta[i] * self.layer.neurons[j]
                    self.error[j] += self.layer.weights[j][i] * self.next.errorDelta[i]
                self.accMatrixDelta[self.biasRow][i] += self.next.errorDelta[i]

            if self.layer.isHidden:
                self.errorDelta = self.error * self.calcDelta()

    def learn(self, learnRate, momentum):
        """Matrix manipulation for learning algorithm"""
        if self.layer.weights is not None:
            self.matrixDelta = self.accMatrixDelta * learnRate + self.matrixDelta * momentum
            self.layer.weights += self.matrixDelta
            self.accMatrixDelta[:] = 0

