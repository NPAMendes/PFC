# Importando bibliotecas necessarias
import numpy as np
import csv

# Leitura do arquivo CSV
with open('ControladorCampo.csv', 'r') as arquivo:
    leitor = csv.reader(arquivo)
    i = list(leitor)

# Definiindo as variáveis de interesse
time = []
tensao_real = []
tensao_desejada = []
corrente_desejada = []
corrente_real = []

# Lendo as variáveis de interesse
for a in i:
    if a[0] != 'Time':
        time.append(float(a[0]))
        tensao_real.append(float(a[5]))
        tensao_desejada.append(float(a[6]))
        corrente_desejada.append(float(a[7]))
        corrente_real.append(float(a[2]))

# Covertndo as listas em vetores
time = np.array(time)
tensao_real = np.array(tensao_real)
tensao_desejada = np.array(tensao_desejada)
corrente_desejada = np.array(corrente_desejada)
corrente_real = np.array(corrente_real)

# Definindo variáveis de erro
corrente = corrente_real - corrente_desejada
tensao = tensao_real - tensao_desejada

#Definindo período de amostragem
T = time[1] - time[0]

# Definindo valores do IAE
IAEc = np.trapz(abs(corrente), dx = T)
IAEt = np.trapz(abs(tensao), dx = T)

# Definindo valores do ITAE
ITAEc = np.trapz(abs(corrente)*time, dx = T)
ITAEt = np.trapz(abs(tensao)*time, dx = T)
