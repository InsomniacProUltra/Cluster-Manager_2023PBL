
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# load the row data from the volume 
x=np.load('x4linear_regression.npy')
y=np.load('y4linear_regression.npy')
# Number of data points
n = len(x)
# Plot of Training Data
plt.scatter(x, y)
plt.xlabel('x')
plt.ylabel('y')
plt.title("Training Data")
plt.show()

#setup the linear regression
# Parameters.
learning_rate = 0.001
training_epochs = 5000
display_epoch = 50
saved_path='/app/miniproject3_result.txt'
 
# Training Data.
X = np.array(x,dtype=float)
Y = np.array(y,dtype=float)
 
# Weight and Bias, initialized randomly.
W = tf.Variable(np.random.randn(), name="weight")
b = tf.Variable(np.random.randn(), name="bias")
 
# Linear regression (W * x + b).
def linear_regression(x):
    return W * x + b
# loss_func: Mean Squared Error
def loss_func(y_pred, y_true):
    return ( tf.reduce_sum(tf.pow(y_pred - y_true, 2)) / (2 * n) )

# Stochastic Gradient Descent Optimizer.
optimizer = tf.optimizers.SGD(learning_rate)

# Run training for the given number of steps.
for epoch in range(training_epochs):
    # Run the optimization to update W and b values.
    # Wrap computation inside a GradientTape for automatic differentiation.
    with tf.GradientTape() as g:
        pred = linear_regression(X)
        loss = loss_func(pred, Y)
        # Compute gradients.
        gradients = g.gradient(loss, [W, b])
        # Update W and b following gradients.
        optimizer.apply_gradients(zip(gradients, [W, b]))

    if (epoch+1) % display_epoch == 0:
        pred = linear_regression(X)
        loss = loss_func(pred, Y)
        print("Epoch", (epoch + 1), ": loss =", loss.numpy(), "Weight =", W.numpy(), "bias =", b.numpy())

        try:
            file = open(saved_path, "a")
            file.write(f"Epoch{epoch + 1}:loss={loss.numpy()},Weight={W.numpy()},bias={b.numpy()}")
            file.write("\n")
            file.close()   
        except FileNotFoundError:
            print("FileNotFound!")
        except IOError:
            print("IOError relating file occured!")
    
# Storing necessary values to be used outside the Session
pred = linear_regression(X)
training_loss = loss_func(pred, Y).numpy()
weight = W.numpy()
bias = b.numpy()
try:
    file = open(saved_path, "a")
    file.write(f"{training_epochs}epochs finished:training loss={training_loss},Weight={weight},bias={bias}")
    file.write("\n")
    file.close()   
except FileNotFoundError:
    print("FileNotFound!")
except IOError:
    print("IOError relating file occured!")

print("\n")
print("Training loss =", training_loss, "Weight =", weight, "bias =", bias)
plt.plot(X, Y, 'ro', label='Original data')
plt.plot(X, pred, label='Fitted line')
plt.legend()
plt.show()