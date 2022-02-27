import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

Force = np.array([0, 0.0682, 0.182, 0.295, 0.408, 0.522, 0.635, 0.748, 0.975])*9.81
Tension = np.array([0.65, 0.97, 1.51, 2, 2.57, 3.1, 3.62, 4.14, 5.12]).reshape((-1, 1))

pressure_front = np.array([12.7, 13.6, 13.7, 13.4, 12.55]) # pressure in mm H2O from -10° to 10°
#pressure_all = np.array([13.7, 12.55, 9.3, 4.1, -2.4, -9.65, -15.45, -18.2, -16.05, -15.1, -14.9, -15, -15.2, -15.2, -15.85, -16.35, -16.7, -16.7, -17]) # pressure in mm H2O from 0° to 180°
pressure_all = np.array([14.06,13.43,10.25,4.63,-2.57,-9.82,-15.9,-19.2,-17.2,-16,-15.8,-16.1,-16,-16,-16.8,-16.5,-17.2,-17.4,-16.8]) # pressure in mm H2O from 0° to 180°
pressure_front *= 9.80665 # conversion from mm H2O to Pa
pressure_all *= 9.80665
angles = np.linspace(0,180,19)

#%% Calibration of drag force

reg = LinearRegression().fit(Tension, Force)
a = reg.coef_[0]; b = reg.intercept_

plt.figure(figsize=(7,4))
plt.xlabel("Tension [V]")
plt.ylabel("Force [N]")
#plt.title("Linear regression of the drag force")
plt.grid()

x = np.linspace(Tension[0]*0.7, Tension[-1]*1.05, 100)
plt.plot(x, a*x+b)

plt.plot(Tension, Force, "o")

Tension_mesuree = 2.94 #V
Force_mesuree = a * Tension_mesuree + b
print("Measured drag: {:.3f}N".format(Force_mesuree))

plt.plot([Tension_mesuree], [Force_mesuree], 'xr', markersize=20)

plt.tight_layout()
plt.savefig("fig1.png", dpi=300)

#%% Pressure around the stagnation point

plt.figure(figsize=(7,4))
plt.xlabel("Angle [°]")
plt.ylabel("Static pressure [Pa]")
#plt.title("Measured static pressure around the stagnation point")
plt.grid()

coefs = np.polyfit(np.array([-10, -5, 0, 5, 10]), pressure_front, 2)
x = np.linspace(-10,10,100)
a = coefs[0]; b = coefs[1]; c = coefs[2]
plt.plot(x, a*x**2 + b*x + c, '--')

p_max = a*(-b/2/a)**2 + b*(-b/2/a) + c
print("max dynamic pressure at alpha = {:.3f}° and p = {:.2f}Pa".format(-b/2/a, p_max))

plt.plot([-10, -5, 0, 5, 10], pressure_front, 'o-')
plt.plot([-b/2/a], [a*(-b/2/a)**2 + b*(-b/2/a) + c], 'xg', markersize=10)

plt.legend(['parabolic interpolation', 'measured pressure', 'maximum'])
plt.tight_layout()
plt.savefig("fig3.png", dpi=300)

#%% Computation of U_inf

rho = 1.225
U_inf = np.sqrt(2*p_max/rho)
Re = U_inf*0.05/15.6e-6

print("Upstream velocity : {:.2f} m/s".format(U_inf))
print("Re = {:.3f} x 10^4".format(Re/1e4))

#%% Pressure along the cylinder

PF_pressure = 2*np.cos(2*angles*np.pi/180) - 1
pressure_coefficient = pressure_all/(0.5*rho*U_inf**2)

plt.figure(figsize=(7,4))
plt.xlabel("angle [°]")
plt.ylabel("Pressure coefficient")
#plt.title("Pressure coefficient along the cylinder")
plt.grid()

plt.plot(angles, pressure_coefficient)
plt.plot(angles, PF_pressure)

plt.legend(["Measured pressure coefficient", "Potential flow pressure coefficient"])
plt.tight_layout()
plt.savefig("fig2.png", dpi=300)

#%% Computation of the drag coefficient

F_drag = 0

for i, theta in enumerate(angles):
    F_drag += pressure_all[i]*np.cos(theta*np.pi/180)
F_drag *= 2*0.5*0.025*(10*np.pi/180)

print("Computed drag : {:.3f} N (vs {:.3f} N)".format(F_drag, Force_mesuree))

print("C_D calculé: {:.3f}".format(F_drag/(0.5*rho*U_inf**2*0.5*0.05)))
print("C_D mesuré: {:.3f}".format(Force_mesuree/(0.5*rho*U_inf**2*0.5*0.05)))
print("C_D mesuré sans plates: {:.3f}".format(Force_mesuree/(0.5*rho*U_inf**2*0.5*0.05) - 0.09))


