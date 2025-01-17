import numpy as np # Importando biblioteca numpy
import matplotlib.pyplot as plt # Importando a biblioteca Matplotlib.pyplot

"""
Máquina trifásica
"""
# Inicializando parâmetros necessários ao programa
r1 = 0.45 # Resistência 1
r2 = 0.416 # Resistência 2
rc = 57.51 # Resistência do núcleo
x1 = 0.83 # Indutância 1
x2 = x1 # Indutânicia 2
xm = 12.64 # Indutância do núcleo
v_phase = 220*np.sqrt(2) # Tensão de fase do circuito
n_sync = 1800 # Velocidade síncrona em RPM
w_sync = n_sync*np.pi/30 # Velocidade síncrona em rad/s
Vth = 118.81 # Tensão de Thevenin
rth = 0.404 # Resistência de Thevenin
xth = 0.779 # Indutência de Thevenin

s = np.arange(1,-1,-0.001) # Definindo o escorregamento
nm = (1-s)*n_sync # Velocidade mecânica

t = np.zeros(len(s)) # Definindo o vetor de torque

# Calculando o conjugado eletromagnético para o rotor
t = (3*Vth**2*r2/s)/(w_sync*((rth + r2/s)**2 + (xth + x2)**2))

plt.figure(1)
plt.plot(nm, t, label= "Curva do torque da MI")
plt.ylabel('Torque Mecâninco (N.m)', fontsize=14)
plt.xlabel('Velocidade do rotor (RPM)', fontsize=14)
plt.grid()

"""
Máquina CC
"""
ra = 2.73 # Resistência de Armadura

n_exp = [1833, 1833, 1829, 1819, 1808, 1796, 1782, 1771, 1758, 1745, 1738]
i_exp = [-10.8, -11.15, -9.77, -6.6, -3.52, 0.421, 2.81, 5.9, 9.21, 12.5, 15.4]
v_exp = [254, 255, 253, 249, 243, 234, 224, 212, 199, 184, 175]
t_exp = np.zeros(11)

for i in np.arange(0,11,1):
    t_exp[i] = (v_exp[i]*i_exp[i] - ra*i_exp[i]**2)/(n_exp[i]*np.pi/30)
    
for i in t_exp:
    print(np.round(i,2))

plt.figure(1)
plt.plot(n_exp, t_exp, label= "Dados do experimento", color = "red", marker='*', linestyle='None')
plt.plot([-300, 4000], [0,0], color = 'k')
plt.plot([0,0],[-100, 100], color = 'k')
plt.xlim([-100, 3700])
plt.ylim([-95,60])
plt.legend()