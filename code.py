import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

Force = np.array([0, 0.0682, 0.182, 0.295, 0.408, 0.522, 0.635, 0.748, 0.975])*9.81
Tension = np.array([0.65, 0.97, 1.51, 2, 2.57, 3.1, 3.62, 4.14, 5.12]).reshape((-1, 1))

#%% Calibration of drag force

reg = LinearRegression().fit(Tension, Force)
a = reg.coef_[0]; b = reg.intercept_

plt.figure(figsize=(7,4))
plt.xlabel("Tension [V]")
plt.ylabel("Force [N]")
plt.grid()

x = np.linspace(Tension[0]*0.7, Tension[-1]*1.05, 100)
plt.plot(x, a*x+b, 'b')

plt.plot(Tension, Force, "or")

Tension_mesuree = 2.94 #V
Force_mesuree = a * Tension_mesuree + b
print("Drag: {:.3f}N".format(Force_mesuree))

plt.plot([Tension_mesuree], [Force_mesuree], 'xg', markersize=20)

plt.tight_layout()
plt.savefig("fig1.png", dpi=300)

#%% Pressure along the cylinder

pressure_front = np.array([12.7, 13.6, 13.7, 13.4, 12.55]) # pressure in mm H2O from -10° to 10°
pressure_all = np.array([13.7, 12.55, 9.3, 4.1, -2.4, -9.65, -15.45, -18.2, -16.05, -15.1, -14.9, -15, -15.2, -15.2, -15.85, -16.35, -16.7, -16.7, -17]) # pressure in mm H2O from 0° to 180°
pressure_front *= 9.80665 # conversion from mm H2O to Pa
pressure_all *= 9.80665
angles = np.linspace(0,180,19)

plt.figure(figsize=(7,4))
plt.xlabel("angle [°]")
plt.ylabel("pressure [Pa]")
plt.title("measured pressure along the cylinder")
plt.grid()

plt.plot(angles, pressure_all, 'k')

plt.savefig("fig2.png", dpi=300)

#%% Pressure around the stagnation point

plt.figure(figsize=(7,4))
plt.xlabel("angle [°]")
plt.ylabel("pressure [Pa]")
plt.title("measured pressure around the stagnation point")
plt.grid()

coefs = np.polyfit(np.array([-10, -5, 0, 5, 10]), pressure_front, 2)
x = np.linspace(-10,10,100)
a = coefs[0]; b = coefs[1]; c = coefs[2]
plt.plot(x, a*x**2 + b*x + c, '--')

p_max = a*(-b/2/a)**2 + b*(-b/2/a) + c
print("max dynamic pressure at alpha = {:.3f}° and p = {:.2f}Pa".format(-b/2/a, p_max))
plt.plot([-b/2/a], [a*(-b/2/a)**2 + b*(-b/2/a) + c], 'xg', markersize=10)

plt.plot([-10, -5, 0, 5, 10], pressure_front, 'o-')

plt.legend(['parabolic interpolation', 'actual data'])

plt.savefig("fig3.png", dpi=300)

#%% Computation of U_inf

rho = 1.225
U_inf = np.sqrt(2*p_max/rho)

print("Upstream velocity : {:.2f} m/s".format(U_inf))

#%%

