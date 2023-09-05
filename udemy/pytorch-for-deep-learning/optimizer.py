import torch
from torch.autograd import Variable

# Simulated data
n = 5  # Number of assets
T = 100  # Number of time periods
returns = torch.randn(n, T)

# Covariance matrix
cov_matrix = returns.mm(returns.t()) / T

# Portfolio weights as a variable
w = Variable(torch.ones(n) / n, requires_grad=True)

# Optimizer
# Adam = Adaptive Moment Estimation
optimizer = torch.optim.Adam([w], lr=0.01)

num_epochs = 1000
for epoch in range(num_epochs):
    optimizer.zero_grad()

    # Portfolio variance
    port_variance = w @ cov_matrix @ w

    # Constraints
    weight_sum = torch.sum(w)
    weight_constraint = torch.abs(weight_sum - 1.0) * 10  # Multiply by a constant to give it more weight
    non_negative_weights = torch.clamp(-w, min=0)  # Negative values are penalized

    # Total loss
    loss = port_variance + weight_constraint + torch.sum(non_negative_weights)

    loss.backward()
    optimizer.step()

    # Project weights to ensure they sum to 1 (this is a simple way to handle the constraint)
    with torch.no_grad():
        w /= torch.sum(w)

print("Optimal weights:", w)
