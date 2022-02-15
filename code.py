import numpy as np
from sklearn.linear_model import LinearRegression

Force = np.array([0, 0.0682, 0.182, 0.295, 0.408, 0.522, 0.635, 0.748, 0.975])*9.81
Tension = np.array([0.65, 0.97, 1.51, 2, 2.57, 3.1, 3.62, 4.14, 5.12]).reshape((-1, 1))

reg = LinearRegression().fit(Tension, Force)
a = reg.coef_[0]; b = reg.intercept_

print(a,b)

Tension_mesuree = 2.9 # TODO

print("Drag: {:.3f}N".format(a * Tension_mesuree + b))