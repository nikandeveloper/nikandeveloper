import numpy as np 
import random
np.random.seed(random.randint())

layers = [2, 2, 2]

w = {}
b = {}
z = {}
a = {}
delta = {}

for l in range(1, len(layers)):
    w[l] = np.random.randn(layers[l], layers[l-1])
    b[l] = np.zeros((layers[l], 1))


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_deriv(a):
    return a * (1-a)

def forward_pass(x):
    a[0] = x.reshape(-1, 1)
    for l in range(1, len(layers)):
        z[l] = w[l] @ a[l - 1] + b[l]
        a[l] = sigmoid(z[l])
    return a[len(layers)-1]

def backward_pass(y):
    L = len(layers) - 1
    y = y.reshape(-1, 1)

    delta[L] = (a[L] - y) * sigmoid_deriv(a[L])   

    for l in reversed(range(1, L)):
        delta[l] = (w[l + 1].T @ delta[l + 1]) * sigmoid_deriv(a[l])    

def update_weigths(lr=0.01):
    for l in range(1, len(layers)):
        dw = delta[l] @ a[l - 1].T
        db = delta[l]

        w[l] -= lr * dw 
        b[l] -= lr * db

def train(x, y, lr=0.1):
    forward_pass(x)
    backward_pass(y)
    update_weigths(lr)

x = np.array([1.0, 0.5])
y = np.array([1.0, 0.0])
lr = 1

for i in range(5):
   for f in range(100000): 
    train(x, y, lr)
   lr *= 0.1
print(forward_pass(x).flatten())
print(y)    