# Importando bibliotecas necessarias
import numpy as np
import csv

# Leitura do arquivo CSV
with open('ControladorNegativo4Q.csv', 'r') as arquivo:
    leitor = csv.reader(arquivo)
    i = list(leitor)

# Definiindo as variáveis de interesse
time = []
torque = []
torqueRef = []

# Lendo as variáveis de interesse
for a in i:
    if (a[0] != 'Time' and float(a[0])>15 and float(a[0])<20):
        time.append(float(a[0]))
        torque.append(float(a[3]))
        torqueRef.append(float(a[5]))

# Covertndo as listas em vetores
time = np.array(time)-15
torque = np.array(torque)
torqueRef = np.array(torqueRef)

# Definindo variáveis de erro
erro = torqueRef - torque

#Definindo período de amostragem
T = time[1] - time[0]

# Definindo valores do IAE
IAE = np.trapz(abs(erro), dx = T)

# Definindo valores do ITAE
ITAE = np.trapz(abs(erro)*time, dx = T)