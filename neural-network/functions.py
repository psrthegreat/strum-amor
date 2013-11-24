"""Activation functions and derivatives for backpropagation"""

import math

class Linear:
    def f(self, x):
        return x
    def df(self, x):
        return 1

class Sigmoid:
    def f(self, x):
        return 1 / (1 + math.exp(-1 * x))
    def df(self, x):
        return x * (1 - x)

class TanH:
    def f(self, x):
        return (math.exp(2 * x) - 1) / (math.exp(2 * x) + 1)
    def df(self, x):
        return 1 - (math.pow(self.f(x), 2))

