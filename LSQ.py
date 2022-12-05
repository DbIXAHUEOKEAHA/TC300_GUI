import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

def f(x, a, b): #simple linear approximation
    return a * x + b

p0=np.array([1, 0]) #initial guess

data_x = [1, 2, 3, 4, 5] 

data_y = [1.1, 2.1, 3.4, 4.4, 5.6]

beta_opt, beta_cov = optimize.curve_fit(f, data_x, data_y, p0)

print(beta_opt)

beta_perr = np.sqrt(np.diag(beta_cov))

plt.plot(data_x, data_y, 'o', color = 'blue', label = 'data')
t = np.linspace(np.min(data_x), np.max(data_x), 1000)
plt.plot(t, f(t, *beta_opt), '-', color = 'red', label = 'lsq')
plt.title(r'LSQ')
plt.xlabel('x data')
plt.ylabel(r'y data')
plt.savefig('LSQ_example.png', dpi = 300)


