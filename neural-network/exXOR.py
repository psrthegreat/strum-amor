import numpy
from network import *

input = numpy.array([[0, 0],
                     [1, 0],
                     [0, 1],
                     [1, 1]])
ideal = numpy.array([[0],
                     [1],
                     [1],
                     [0]])

network = Network()
network.addLayer(Layer(2))
network.addLayer(Layer(3))
network.addLayer(Layer(1))
network.reset()

train = Backpropagation(network, input, ideal, 0.7, 0.9)
for epoch in range(1, 1000):
    train.iteration()
    print("Epoch #" + str(epoch) + " Error: " + str(train.error))

    if train.error < 0.001:
        break

print("Neural Network Results:")
for i in range(len(ideal)):
    actual = network.computeOutputs(input[i])
    print(str(input[i]) + " Actual: " + str(actual[0]) + " Ideal: " + str(ideal[i][0]))

