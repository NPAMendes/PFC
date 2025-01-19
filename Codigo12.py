import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

ra = 2.73 # Resistência de Armadura

n_exp = [1833, 1833, 1829, 1819, 1808, 1796, 1782, 1771, 1758, 1745, 1738]
i_exp = [-10.8, -11.15, -9.77, -6.6, -3.52, 0.421, 2.81, 5.9, 9.21, 12.5, 15.4]
v_exp = [254, 255, 253, 249, 243, 234, 224, 212, 199, 184, 175]
t_exp = np.zeros(11)

for i in np.arange(0,11,1):
    t_exp[i] = (v_exp[i]*i_exp[i] - ra*i_exp[i]**2)/(n_exp[i]*np.pi/30)
    
def modelo(corrente, K, c):
    return (K * corrente)

# Ajuste do modelo aos dados
popt, pcov = curve_fit(modelo, i_exp, t_exp)

# O valor estimado de K
K = popt[0]
#c = popt[1]


ia = np.arange(i_exp[0], i_exp[-1] + 0.001, 0.001)
plt.figure()
plt.plot(i_exp,t_exp, '*b', label = 'Dados da Simulação')
plt.plot(ia, ia*K, 'r', label = 'Aproximação')
plt.plot([-100,100],[0,0], 'k' )
plt.plot([0,0],[-100,100], 'k' )
plt.xlim([-35,30])
plt.ylim([-25,20])
plt.xlabel('Corrente de Armadura (A)', fontsize=18)
plt.ylabel('Torque (Nm)', fontsize=18)
plt.grid()
plt.legend(fontsize = 18)