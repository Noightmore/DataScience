import numpy as np

"""

matlab:
    A = 3
    B = 1
    C = .1
    sigma2 = 1
    
    N = 100
    H = [ones(N, 1) (1:N) (1:N).^2];
    hatTheta = H'*H)\(H'*x);
    w = randn(N, 1) * sqrt(sigma2);
    
    trials = 100
    
    for trial = 1:trials
        x = H * [A; B; C] + w;
        hatTheta(:, trial) = (H'*H)\(H'*x);
    end

"""

# python:
A = 3
B = 1
C = .1

sigma2 = 1
mean = 0
N = 1000
H = np.vstack((np.ones(N), np.arange(N), np.arange(N)**2)).T
w = np.random.randn(N + mean) * np.sqrt(sigma2)

trials = 100

hatTheta = np.zeros((3, trials))

for trial in range(trials):
    x = H @ np.array([A, B, C]) + w
    hatTheta[:, trial] = np.linalg.inv(H.T @ H) @ H.T @ x

#print(hatTheta)

# print means of the columns

print(np.mean(hatTheta, axis=1))
