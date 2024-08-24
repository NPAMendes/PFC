import numpy as np # Importando biblioteca numpy
import matplotlib.pyplot as plt # Importando a biblioteca Matplotlib.pyplot
import csv

# Leitura do arquivo CSV
with open('SimulacaoCompleta.csv', 'r') as arquivo:
    leitor = csv.reader(arquivo)
    i = list(leitor)

# Definiindo as variáveis de interesse
torque = []
velocidade = []

# Lendo as variáveis de interesse
for a in i:
    if (a[0] != 'Time' and float(a[0])> 10):
        torque.append(float(a[3]))
        velocidade.append(float(a[4]))
        
# Covertndo as listas em vetores
torque = np.array(torque)
velocidade = np.array(velocidade)

plt.figure(1)
plt.plot(velocidade, torque, label= "Dados da Simulação", color = "red", marker='*', linestyle='None')
plt.plot([-300, 4000], [0,0], color = 'k')
plt.plot([0,0],[-100, 100], color = 'k')
plt.xlim([-100, 3700])
plt.ylim([-95,60])

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
plt.legend()