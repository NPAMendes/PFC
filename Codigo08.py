# Importando bibliotecas necessarias
import numpy as np
import csv

# Leitura do arquivo CSV
with open('SimulacaoCompleta.csv', 'r') as arquivo:
    leitor = csv.reader(arquivo)
    i = list(leitor)

# Definiindo as variáveis de interesse
time = [[],[],[],[],[],[],[]]
torque = [[],[],[],[],[],[],[]]
torqueRef = [[],[],[],[],[],[],[]]

# Lendo as variáveis de interesse
for a in i:
    k = -1
    if (a[0] != 'Time'):
        if (float(a[5]) == -15): k = 0
        elif (float(a[5]) == -10): k=1
        elif (float(a[5]) == -5): k=2
        elif (float(a[5]) == 0): k=3
        elif (float(a[5]) == 5): k=4
        elif (float(a[5]) == 10): k=5
        elif (float(a[5]) == 15): k=6
    if (k != -1):
        time[k].append(float(a[0]))
        torque[k].append(float(a[3]))
        torqueRef[k].append(float(a[5]))
        

# Covertndo as listas em vetores
for i in range(7):
    time[i] = np.array(time[i])
    torque[i] = np.array(torque[i])
    torqueRef[i] = np.array(torqueRef[i])

for i in range(7):
    time[i] = time[i] - time[i][0]

# Definindo variáveis de erro
erro = []

for i in range(7):
    erro.append(torqueRef[i] - torque[i])

#Definindo período de amostragem
T = time[0][1] - time[0][0]

# Definindo valores do IAE e ITAE
IAE = []
ITAE = []

for i in range(7):
    IAE.append(np.trapz(abs(erro[i]), dx = T))
    ITAE.append(np.trapz(abs(erro[i])*time[i], dx = T))