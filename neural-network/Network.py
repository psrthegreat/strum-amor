import math
import numpy

class Network:
    def __init__(self):
        self.layers = []
        self.inputLayer = None
        self.outputLayer = None

    def addLayer(self, layer):
        if self.outputLayer is not None:
            layer.previous = self.outputLayer
            self.outputLayer.next = layer
            self.outputLayer.matrix = numpy.zeros((self.outputLayer.neuronCount + 1, self.outputLayer.neuronCount))

        if len(self.layers) == 0:
            self.inputLayer = self.outputLayer = layer
        else:
            self.outputLayer = layer

        self.layers.append(layer)

    def calcError(self, input, ideal):
        # Calculate RMS
        actual = numpy.array([self.computeOutputs(inputVec) for inputVec in input])
        return numpy.linalg.norm(ideal - actual) / math.sqrt(len(ideal));

    def computeOutputs(self, input):
        for layer in self.layers:
            if layer.isInput():
                layer.computeOutputs(input)
            elif layer.isHidden():
                layer.computeOutputs()

        return self.outputLayer.fire

