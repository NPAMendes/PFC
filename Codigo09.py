# Importando bibliotecas necessarias
import numpy as np
import csv
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt # Importando biblioteca para plotagem de graficos

# Leitura do arquivo CSV
with open('SimulacaoCompleta.csv', 'r') as arquivo:
    leitor = csv.reader(arquivo)
    i = list(leitor)

# Definiindo as variáveis de interesse
torque = []
ia = []

# Lendo as variáveis de interesse
for a in i:
    if (a[0] != 'Time' and float(a[0])>10):# and (float(a[0])<49.9 or float(a[0])>50.1)):
        torque.append(float(a[3]))
        ia.append(float(a[1]))
        
# Covertndo as listas em vetores
torque = np.array(torque)
ia = np.array(ia)

# Definição do modelo de ajuste
def modelo(corrente, K, c):
    return (K * corrente + c)

# Ajuste do modelo aos dados
popt, pcov = curve_fit(modelo, ia, torque)

# O valor estimado de K
K = popt[0]
c = popt[1]

plt.figure()
plt.plot(ia,torque, '*b', label = 'Dados da Simulação')
plt.plot(ia, ia*K+c, 'r', label = 'Aproximação')
plt.plot([-100,100],[0,0], 'k' )
plt.plot([0,0],[-100,100], 'k' )
plt.xlim([-35,30])
plt.ylim([-25,20])
plt.xlabel('Corrente de Armadura (A)', fontsize=18)
plt.ylabel('Torque (Nm)', fontsize=18)
plt.grid()
plt.legend(fontsize = 18)
