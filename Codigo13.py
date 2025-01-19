import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

ra = 2.73 # Resistência de Armadura

n_exp = [1833, 1833, 1829, 1819, 1808, 1796, 1782, 1771, 1758, 1745, 1738]
i_exp = [-10.8, -11.15, -9.77, -6.6, -3.52, 0.421, 2.81, 5.9, 9.21, 12.5, 15.4]
v_exp = [254, 255, 253, 249, 243, 234, 224, 212, 199, 184, 175]
main = [-100, -80.8, -60, -40, -20.3, 0.4, 20.7, 40.2, 60.4, 80.7, 100]
t_exp = np.zeros(11)

for i in np.arange(0,11,1):
    t_exp[i] = (v_exp[i]*i_exp[i] - ra*i_exp[i]**2)/(n_exp[i]*np.pi/30)
    
def modelo(main, K1, K2, K3, K4, K5, c):
    return (K5*main**5 + K4*main**4 + K3*main**3 + K2*main**2 + K1*main + c)

# Ajuste do modelo aos dados
popt, pcov = curve_fit(modelo, main, t_exp)

# O valor estimado de K
K1, K2, K3, K4, K5, c = popt


mains = np.arange(main[0], main[-1] + 0.001, 0.001)

plt.figure(1)
plt.subplot(211)
plt.plot(main,t_exp, '*b', label = 'Dados da Simulação')
plt.plot(mains, K5*mains**5 + K4*mains**4 + K3*mains**3 + K2*mains**2 + K1*mains + c, 'r', label = 'Aproximação')
plt.plot([-200,200],[0,0], 'k' )
plt.plot([0,0],[-100,100], 'k' )
plt.xlim([-110,110])
plt.ylim([-20,15])
plt.xlabel('Main setpoint', fontsize=18)
plt.ylabel('Torque (Nm)', fontsize=18)
plt.grid()
plt.legend(fontsize = 18)


def modelo(t, K1, K2, K3, K4, K5, c):
    return (K5*t**5 + K4*t**4 + K3*t**3 + K2*t**2 + K1*t + c)

# Ajuste do modelo aos dados
popt, pcov = curve_fit(modelo, t_exp, main)

# O valor estimado de K
K6, K7, K8, K9, K10, c1 = popt

ts = np.arange(t_exp[0], t_exp[-1] + 0.001, 0.001)

plt.figure(1)
plt.subplot(212)
plt.plot(t_exp,main, '*b', label = 'Dados da Simulação')
plt.plot(ts, K10*ts**5 + K9*ts**4 + K8*ts**3 + K7*ts**2 + K6*ts + c1, 'r', label = 'Aproximação')
plt.plot([-200,200],[0,0], 'k' )
plt.plot([0,0],[-100,100], 'k' )
plt.ylim([-110,110])
plt.xlim([-20,15])
plt.ylabel('Main setpoint', fontsize=18)
plt.xlabel('Torque (Nm)', fontsize=18)
plt.grid()
plt.legend(fontsize = 18)