import numpy as np
import scipy.io
import matplotlib.pyplot as plt

mat_data = scipy.io.loadmat('./RIRidentification.mat')

# variables: fs, u, x

print(mat_data.keys())

fs = mat_data['fs'][0][0]
u = mat_data['u']
x = mat_data['x']

#print(fs)
#print(u)
#print(x)

p = 400 # doporuceno 1000

"""
    matlab: 
    p = 1000;
    H = toeplitz(u, [u(1) zeros(1, p-1)]);
    hhat = (H'*H)\(H'*x);
    plot(hhat)
    320/fs*115
"""

H = scipy.linalg.toeplitz(u, np.hstack((u[0], np.zeros(p-1))))
hhat = np.linalg.inv(H.T @ H) @ H.T @ x
#print(hhat)
plt.plot(hhat)




