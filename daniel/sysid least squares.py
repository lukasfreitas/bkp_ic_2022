import scipy.signal
import numpy as np
import matplotlib.pyplot as plt

# Continuous transfer function of a process
Ts = 0.1
#Pd = scipy.signal.TransferFunction([7], [1, -0.3], dt=Ts) # discrete
P = scipy.signal.TransferFunction([7], [1, 3, 11]) # continuous

# Discrete process for simulation
Pd = P.to_discrete(Ts)
print('Discrete system:')
print(Pd)

# Simulate system with an input "u"
t = np.arange(0, 5, Ts)
u = np.ones_like(t)
u[0:5] = 0 # initial input as zeros to establish a baseline
tout, y = scipy.signal.dlsim(Pd, u, t)

# remove unneeded extra dimension from y
y = y.flatten()

npts = len(y)
nbd = 1 # discrete zeros order (2 coefficients)
nad = 2 # discrete poles order (3 coefficients)

# Ordinary Least Squares (OLS)
# phi*theta = Y
Y = []
phi = []
print("UUUUU ",u)
for j in range(max(nad,nbd)+1, npts-1):
    phirow = []
    
    for i in range(nad):
        phirow.append(-y[j-i-1])

    for i in range(nbd+1):
        phirow.append(u[j-i-1])

    Y.append([y[j]])
    phi.append(phirow)

Y = np.array(Y)
phi = np.array(phi)

# Example 1 - raw computation of matrix solution
#theta = np.linalg.pinv(phi.T@phi)@phi.T@Y
#print(theta)

# Example 2 - should be used - lstsq does some additional numerical work
theta, _, _, _ = np.linalg.lstsq(phi, Y, rcond=None)
#print(theta)

theta = theta.flatten()

B = theta[nad:]
A = np.concatenate(([1], theta[:nad]))
print('B/A model')
print(B)
print(A)

# Process model
Pmd = scipy.signal.TransferFunction(B, A, dt=Ts) # discrete

# Simulate model with an input "u"
tout, ym = scipy.signal.dlsim(Pmd, u, t)



# Plot time response
fig, ax = plt.subplots(2, sharex=True)
ax[0].plot(tout, ym, 'b--')
ax[0].plot(tout, y, 'k.')
ax[0].set_ylabel('y(t)')
ax[1].plot(tout, u) # extend u to match tout shape
ax[1].set_ylabel('u(t)')
plt.xlabel('t (s)')
plt.xlim(t[0], t[-1])
plt.show()