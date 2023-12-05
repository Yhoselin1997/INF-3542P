import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

iris = load_iris()
X, y = iris.data, iris.target

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

input_size = X.shape[1]
hidden_size = 5
output_size = 3

weights_input_hidden = np.random.rand(input_size, hidden_size)
weights_hidden_output = np.random.rand(hidden_size, output_size)

learning_rate = 0.01
epochs = 10000

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

for epoch in range(epochs):
    hidden_input = np.dot(X_train, weights_input_hidden)
    hidden_output = sigmoid(hidden_input)

    final_input = np.dot(hidden_output, weights_hidden_output)
    final_output = sigmoid(final_input)

    output_error = y_train.reshape(-1, 1) - final_output
    output_delta = output_error * sigmoid_derivative(final_output)

    hidden_error = output_delta.dot(weights_hidden_output.T)
    hidden_delta = hidden_error * sigmoid_derivative(hidden_output)

    weights_hidden_output += hidden_output.T.dot(output_delta) * learning_rate
    weights_input_hidden += X_train.T.dot(hidden_delta) * learning_rate

    if epoch % 1000 == 0:
        print(f"Época {epoch} - Error: {np.mean(np.abs(output_error))}")

hidden_layer_input = np.dot(X_test, weights_input_hidden)
hidden_layer_output = sigmoid(hidden_layer_input)

final_layer_input = np.dot(hidden_layer_output, weights_hidden_output)
final_layer_output = sigmoid(final_layer_input)

print("\nResultados finales en datos de prueba:")
print(final_layer_output)
