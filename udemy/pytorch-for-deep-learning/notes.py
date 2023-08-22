import torch
import numpy as np

# 2. Set the random seed for NumPy and PyTorch both to "42"
np.random.seed(42)
torch.manual_seed(42)

# 3. Create a NumPy array called "arr" that contains 6 random integers between 0 (inclusive) and 5 (exclusive)
arr = np.random.randint(0,5,6)
print(arr)

# 4. Create a tensor "x" from the array above
x = torch.from_numpy(arr)
print(x)

# 5. Change the dtype of x from 'int32' to 'int64'
x = x.type(torch.int64)
# x = x.type(torch.LongTensor)
print(x.type())

# 6. Reshape x into a 3x2 tensor
x = x.view(3,2)
# x = x.reshape(3,2)
# x.resize_(3,2)
print(x)

# 7. Return the right-hand column of tensor x
print(x[:,1:])
# print(x[:,1])

# 8. Without changing x, return a tensor of square values of x
print(x*x)
# print(x**2)
# print(x.mul(x))
# print(x.pow(2))
# print(torch.mul(x,x))

# 9. Create a tensor "y" with the same number of elements as x, that can be matrix-multiplied with x
y = torch.randint(0,5,(2,3))
print(y)

# 10. Find the matrix product of x and y
print(x.mm(y))

#
# Linear Regression
#
# Create a column matrix of X values
X = torch.linspace(1,50,50).reshape(-1,1)

# Create a "random" array of error values
torch.manual_seed(71) # to obtain reproducible results
e = torch.randint(-8,9,(50,1),dtype=torch.float)
print(e.sum())

# Create a column matrix of y values
y = 2*X + 1 + e
print(y.shape)

plt.scatter(X.numpy(), y.numpy())
plt.ylabel('y')
plt.xlabel('x')

torch.manual_seed(59)

model = nn.Linear(in_features=1, out_features=1)
print(model.weight)
print(model.bias)

class Model(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)

    def forward(self, x):
        y_pred = self.linear(x)
        return y_pred

torch.manual_seed(59)
model = Model(1, 1)
print(model)
print('Weight:', model.linear.weight.item())
print('Bias:  ', model.linear.bias.item())

for name, param in model.named_parameters():
    print(name, '\t', param.item())

x = torch.tensor([2.0])
print(model.forward(x))

x1 = np.array([X.min(),X.max()])
print(x1)

w1,b1 = model.linear.weight.item(), model.linear.bias.item()
print(f'Initial weight: {w1:.8f}, Initial bias: {b1:.8f}')
print()

y1 = x1*w1 + b1
print(y1)

plt.scatter(X.numpy(), y.numpy())
plt.plot(x1,y1,'r')
plt.title('Initial Model')
plt.ylabel('y')
plt.xlabel('x');

criterion = nn.MSELoss()

optimizer = torch.optim.SGD(model.parameters(), lr = 0.001)


epochs = 50
losses = []

for i in range(epochs):
    i+=1
    y_pred = model.forward(X)
    loss = criterion(y_pred, y)
    losses.append(loss)
    print(f'epoch: {i:2}  loss: {loss.item():10.8f}  weight: {model.linear.weight.item():10.8f}  \
bias: {model.linear.bias.item():10.8f}')
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

plt.plot(range(epochs), losses)
plt.ylabel('Loss')
plt.xlabel('epoch');

w1,b1 = model.linear.weight.item(), model.linear.bias.item()
print(f'Current weight: {w1:.8f}, Current bias: {b1:.8f}')
print()

y1 = x1*w1 + b1
print(x1)
print(y1)

plt.scatter(X.numpy(), y.numpy())
plt.plot(x1,y1,'r')
plt.title('Current Model')
plt.ylabel('y')
plt.xlabel('x');

# Building train/test split tensors
from sklearn.model_selection import train_test_split

train_X, test_X, train_y, test_y = train_test_split(df.drop('target',axis=1).values,
                                                    df['target'].values, test_size=0.2,
                                                    random_state=33)

X_train = torch.FloatTensor(train_X)
X_test = torch.FloatTensor(test_X)
y_train = torch.LongTensor(train_y).reshape(-1, 1)
y_test = torch.LongTensor(test_y).reshape(-1, 1)

