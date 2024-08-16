# Importando bibliotecas necessarias
import numpy as np
import csv

"""
Definindo parametros
"""

Ra = 2.73 # Resistência de armadura
w = 728*np.pi/30 # Velocidade de rotacao em rad/s
b = 0.00704 # Coeficiente de fiscosidade

"""
Coletando dados de arquivos CSV
"""

# Coletando dados de arquivo CSV do Canal 1
with open('CH1_Inercia.csv', 'r') as arquivo:
    leitor = csv.reader(arquivo)
    i = list(leitor)

# Extraindo dados de tensao e tempo
tensao = [] # Criando vetor que recebera os valores de tensao em Volts
tempo = [] # Criando vetor que recebera os valores de tempo em Segundos

# Criando loop para atribuicao de dados de tensao
for a in i:
    tensao.append(float(a[4]))
    tempo.append(float(a[3]))

# Coletando dados de arquivo CSV do Canal 2
with open('CH2_Inercia.csv', 'r') as arquivo:
    leitor = csv.reader(arquivo)
    i = list(leitor)

# Extraindo dasdos de corrente
corrente = [] # Criando vetor que recebera os valores de Corrente em Amperes

# Criando loob para atribuicao de dados
for a in i:
    corrente.append(float(a[4])/0.2)

"""
Processando dados
"""
corrente = np.array(corrente)
tensao = np.array(tensao)
tempo = np.array(tempo)
    
"""
Calculando energia fornecida
"""
T = np.round(tempo[1] - tempo[0],4) # Definindo periodo de amostragem

Pt = corrente*tensao # Definindo a potencia do sistema

Jt = np.trapz(Pt, dx = T) # Definindo a energia do sistema

"""
Calculando perdas
"""

Pe = Ra*corrente**2 # Potência elétrica
Je = np.trapz(Pe, dx = T) # Energia elétrica

# Construcao do vetor de velocidade
omega = []
for i in tensao:
    if i == 0:
        omega.append(0)
    else:
        omega.append(w)
omega = np.array(omega)

Pm = b*omega**2 # Potencia mecanica

Jm = np.trapz(Pm, dx = T) # Energia Mecanica

"""
Calculando energia cinética
"""
K = Jt - Je - Jm
