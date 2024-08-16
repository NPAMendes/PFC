import csv # Importando biblioteca para analise de arquivos CSV
import numpy as np # Importando biblioteca Numpy
import matplotlib.pyplot as plt # Importando biblioteca para plotagem de graficos
import control as ct # Importando a biblioteca control

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
# Definindo peri�odo de amostragem
T = np.round(tempo[1]-tempo[0], 4)
    
# Estendendo os dados de tensao e corrente
tensao2 = []
corrente2 = []

for k in range(27):
    tensao2.append(tensao[-k-1])
    corrente2.append(corrente[-k-1])

for k in range(2000):
    tensao = [*tensao, *tensao2]
    corrente = [*corrente, *corrente2]

# Estendendo os dados de tempo
tempo = np.arange(tempo[0], len(tensao)*T + tempo[0], T)
tempo = tempo[250:]
    
"""
Criando modelo do sistema
"""

# Parametros de Modelagem
Ra = 2.73 # Resistencia de Armadura
La = 0.01638 # Indutancia de armadura
b = 0.00704 # Coeficiente de viscosidade
J = 0.0236 # Momento de inercia
K = 1.356 # Constate de magnetizacao

# Definindo a funcao de transferencia
G = ct.tf([K], [La*J, La*b + Ra*J, Ra*b + K**2])

# Aplicando o sinal de entrada no sistema
t, omega = ct.forced_response(G, tempo, tensao[250:])

# convertendo omega em RPM
omega = omega*30/np.pi

#Plotando as varaveis de interesse
plt.figure(1)
plt.subplot(311) 
plt.plot(t,omega,'b', label = "Completo")
plt.plot(t,0.95*omega[-1]*np.ones(len(t)),'--k', label = 'Criterio de $2%$')
plt.grid()
plt.ylabel('$\\omega (RPM)$')
plt.xlim(0,0.3)

plt.subplot(312) 
plt.plot(t,tensao[250:],'b')
plt.grid()
plt.ylabel('Tensao (V)')
plt.xlim(0,0.35)

plt.subplot(313) 
plt.plot(t,corrente[250:],'b')
plt.grid()
plt.ylabel('Corrente (A)')
plt.xlabel('Tempo (s)')
plt.xlim(0,0.35)

"""
Repetinndo o processo para sistema de primeira ordem com La = 0
"""

# Definindo a funcao de transferencia
G1 = ct.tf([K], [Ra*J, Ra*b + K**2])

# Aplicando o sinal de entrada no sistema
t, omega1 = ct.forced_response(G1, tempo, tensao[250:])

# convertendo omega em RPM
omega1 = omega1*30/np.pi

#Plotando as varaveis de interesse
plt.figure(1)
plt.subplot(311) 
plt.plot(t,omega1,'g', label = "$L_a = 0 H$")


"""
Repetinndo o processo para sistema de primeira ordem com La = 0 e b = 0
"""

# Definindo a funcao de transferencia
G2 = ct.tf([K], [Ra*J, K**2])

# Aplicando o sinal de entrada no sistema
t, omega2 = ct.forced_response(G2, tempo, tensao[250:])

# convertendo omega em RPM
omega2 = omega2*30/np.pi

#Plotando as varaveis de interesse
plt.figure(1)
plt.subplot(311) 
plt.plot(tempo,omega2,'r', label = "$L_a = 0 H$ e $b=0(N.m)/(rad/s)$")
plt.legend()
plt.axes([0.4, 0.75, 0.4, 0.16])
plt.plot(t,omega,'b')
plt.plot(t,omega1,'g')
plt.plot(t,omega2,'k')
plt.xlim(0.14,0.154)
plt.ylim(640,660)
plt.grid()

"""
Calculando parametros de desempenho
"""

# Definindo variaveis de erro
erro1 = (omega1[0:3000] - omega[0:3000])*np.pi/30
erro2 = (omega2[0:3000] - omega[0:3000])*np.pi/30

# Definindo valores do IAE
IAE1 = np.trapz(abs(erro1), dx = T)
IAE2 = np.trapz(abs(erro2), dx = T)

# Definindo valores do ITAE
ITAE1 = np.trapz(abs(erro1)*tempo[0:3000], dx = T)
ITAE2 = np.trapz(abs(erro2)*tempo[0:3000], dx = T)
