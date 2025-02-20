import numpy as np

"""

sigma2 = 1
N = 1000
A = 3
B = 1
w = np.random.randn(N) * np.sqrt(sigma2)
X = np.zeros(N)

for i in range(N):
    X[i] = (A + B * i + w[i])

#print(X)
"""

"""
    matlab:
    H = [ones(N,1) (1:N)];
    x = H * [A; B] + w;
    hatTheta = (H'*H)\(H'*x);
    
    trials = 100
    
    for trial = 1:trials
        x = H * [A; B] + w;
        hatTheta(:, trial) = (H'*H)\(H'*x);
    
"""


sigma2 = 1
N = 1000
A = 3
B = 1
w = np.random.randn(N) * np.sqrt(sigma2)

# Vectorized operation
indices = np.arange(N)
#X = A + B * indices + w

H = np.vstack((np.ones(N), indices)).T
X = H @ np.array([A, B]) + w
#hatTheta = np.linalg.inv(H.T @ H) @ H.T @ X

trials = 100

hatTheta = np.zeros((2, trials))


for trial in range(trials):
    x = H @ np.array([A, B]) + w
    hatTheta[:, trial] = np.linalg.inv(H.T @ H) @ H.T @ x

print(hatTheta)

"""
    matlab:
    cov(hatTheta')
    sigma2 * inv(H'*H)
"""


#print(f"covariance matrix: {np.cov(hatTheta.T)}")
print(f"sigma2 * inv(H.T @ H): {sigma2 * np.linalg.inv(H.T @ H)}")

# Z is a complex value 1 + 2i
#Z = 1 + 2j

# print z squared
#print("The square of z is", Z * Z)
