import csv # Importando biblioteca para analise de arquivos CSV
import numpy as np # Importando biblioteca Numpy
import matplotlib.pyplot as plt # Importando biblioteca para plotagem de graficos
import control as ct # Importando a biblioteca control

"""
Coletando dados de arquivos CSV
"""

# Coletando dados de arquivo CSV do Canal 1
with open('F0001CH1.csv', 'r') as arquivo:
    leitor = csv.reader(arquivo)
    i = list(leitor)

# Extraindo dados de tensao
tensao = np.zeros(len(i)) # Criando vetor que recebera os valores de tensao em Volts

k = 0 # Inicializando um contador

# Criando loop para atribuicao de dados de tensao
for a in i:
    tensao[k] = float(a[4])
    k=k+1
    
# Extraindo dasdos de tempo
tempo = np.zeros(len(i)) # Criando vetor que recebera os valores de tempo em Segundos

k = 0 # Inicializando um contador

# Criando loop para atribuicao de dados de tempo
for a in i:
    tempo[k] = float(a[3])
    k=k+1

# Coletando dados de arquivo CSV do Canal 2
with open('F0001CH2.csv', 'r') as arquivo:
    leitor = csv.reader(arquivo)
    i = list(leitor)

# Extraindo dasdos de corrente
corrente = np.zeros(len(i)) # Criando vetor que recebera os valores de Corrente em Amperes

k = 0 # Inicializando um contador

# Criando loob para atribuicao de dados
for a in i:
    corrente[k] = float(a[4])/0.2
    k=k+1
    
"""
Criando modelo do sistema
"""

# Parametros de Modelagem
Ra = 2.73 # Resistencia de Armadura
La = 0.01638 # Indutancia de armadura
b = 0.00704 # Coeficiente de viscosidade
J = 0.0236 # Momento de inercia

# Definindo peri­odo de amostragem
T = np.round(tempo[1]-tempo[0], 4)
    
# Estendendo os dados de tensao
tensao2 = np.zeros(27)

for k in range(27):
    tensao2[k] = tensao[-k-1]

for k in range(2000):
    tensao = [*tensao, *tensao2]

# Estendendo os dados de tempo
tempo2 = np.arange(tempo[0], len(tensao)*T + tempo[0], T)
tempo = tempo2

# Estendendo os dados de corrente
corrente2 = np.zeros(27)

for k in range(27):
    corrente2[k] = corrente[-k-1]

for k in range(2000):
    corrente = [*corrente, *corrente2]

# Criando vetor de tempo
t = np.zeros(len(tempo)-250)
t = tempo[250:]

# Definindo a constante da curva de magnetizacao
K = 1.356

# Definindo a função de transferência
G = ct.tf([K], [La*J, La*b + Ra*J, Ra*b + K**2])

# Aplicando o sinal de entrada no sistema
t, omega = ct.forced_response(G, t, tensao[250:])

# convertendo omega em RPM
omega = omega*30/np.pi

#Plotando as varaveis de interesse
plt.figure(1)
plt.subplot(311) 
plt.plot(t,omega,'b', label = "Completo")
plt.plot(t,0.95*omega[-1]*np.ones(len(t)),'--k', label = 'Critério de $2%$')
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

# Definindo a função de transferência
G1 = ct.tf([K], [Ra*J, Ra*b + K**2])

# Aplicando o sinal de entrada no sistema
tempo, omega1 = ct.forced_response(G1, t, tensao[250:])

# convertendo omega em RPM
omega1 = omega1*30/np.pi

#Plotando as varaveis de interesse
plt.figure(1)
plt.subplot(311) 
plt.plot(tempo,omega1,'g', label = "$L_a = 0 H$")


"""
Repetinndo o processo para sistema de primeira ordem com La = 0 e b = 0
"""

# Definindo a função de transferência
G2 = ct.tf([K], [Ra*J, K**2])

# Aplicando o sinal de entrada no sistema
tempo, omega2 = ct.forced_response(G2, t, tensao[250:])

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
#plt.show()

"""
Calculando parametros de desempenho
"""

# Definindo variáveis de erro
erro1 = (omega1[0:3000] - omega[0:3000])*np.pi/30
erro2 = (omega2[0:3000] - omega[0:3000])*np.pi/30

# Definindo variáveis do ISE
ISE1 = 0
ISE2 = 0

# Calculo do ISE
for k in range(len(erro1)):
    if k>0:
        ISE1 = ISE1 + T*(erro1[k]**2 + erro1[k-1]**2)/2
        ISE2 = ISE2 + T*(erro2[k]**2 + erro2[k-1]**2)/2

# Definindo variáveis do ISE
ITSE1 = 0
ITSE2 = 0

# Calculo do ITSE
for k in range(len(erro1)):
    if k>0:
        ITSE1 = ITSE1 + T*k*(erro1[k]**2 + erro1[k-1]**2)/2
        ITSE2 = ITSE2 + T*k*(erro2[k]**2 + erro2[k-1]**2)/2
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        