import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Cargar el dataset iris
iris = load_iris()
X = iris.data
y = iris.target

# Normalizar los datos
X = X / np.amax(X, axis=0)

one_hot_labels = np.zeros((y.size, y.max()+1))
one_hot_labels[np.arange(y.size), y] = 1
y = one_hot_labels

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

input_size = 4
hidden_size = 5
output_size = 3

W1 = np.random.randn(input_size, hidden_size)
W2 = np.random.randn(hidden_size, output_size)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Entrenar la red
epochs = 1000
learning_rate = 0.1
for epoch in range(epochs):
    z1 = np.dot(X_train, W1)
    a1 = sigmoid(z1)
    z2 = np.dot(a1, W2)
    a2 = sigmoid(z2)

    error_out = y_train - a2
    delta_out = error_out * sigmoid_derivative(a2)

    error_hidden = np.dot(delta_out, W2.T)
    delta_hidden = error_hidden * sigmoid_derivative(a1)

    W2 += np.dot(a1.T, delta_out) * learning_rate
    W1 += np.dot(X_train.T, delta_hidden) * learning_rate

z1 = np.dot(X_test, W1)
a1 = sigmoid(z1)
z2 = np.dot(a1, W2)
a2 = sigmoid(z2)

y_pred = np.argmax(a2, axis=1)
y_true = np.argmax(y_test, axis=1)

print("Etiquetas predichas:", y_pred)
print("Etiquetas reales:", y_true)

