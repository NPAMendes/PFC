import csv # Importando biblioteca para analise de arquivos CSV
import numpy as np # Importando biblioteca Numpy
import matplotlib.pyplot as plt # Importando biblioteca para plotagem de graficos
import control as ct # Importando a biblioteca control

plt.close('all')

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
    
corrente = np.array(corrente)
tensao = np.array(tensao)
tempo = np.array(tempo)

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
t, omega = ct.forced_response(G, tempo, tensao)

# convertendo omega em RPM
omega = omega*30/np.pi

#Plotando as varaveis de interesse
plt.figure(1)
plt.subplot(311) 
plt.plot(t,omega,'b', label = "Completo")
plt.plot(t,0.95*omega[-1]*np.ones(len(t)),'--k', label = 'Criterio de $2%$')
plt.grid()
plt.ylabel('$\\omega (RPM)$', fontsize=18)
plt.xlim([0, tempo[-1]])

plt.subplot(312) 
plt.plot(t,tensao,'b')
plt.grid()
plt.ylabel('Tensao (V)', fontsize=18)
plt.xlim([0, tempo[-1]])

plt.subplot(313) 
plt.plot(t,corrente,'b')
plt.grid()
plt.ylabel('Corrente (A)', fontsize=18)
plt.xlabel('Tempo (s)', fontsize=18)
plt.xlim([0, tempo[-1]])

plt.subplots_adjust(
    top=0.984,
    bottom=0.07,
    left=0.042,
    right=0.992,
    hspace=0.145,
    wspace=0.2
)
"""
Repetinndo o processo para sistema de primeira ordem com La = 0
"""

# Definindo a funcao de transferencia
G1 = ct.tf([K], [Ra*J, Ra*b + K**2])

# Aplicando o sinal de entrada no sistema
t, omega1 = ct.forced_response(G1, tempo, tensao)

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
t, omega2 = ct.forced_response(G2, tempo, tensao)

# convertendo omega em RPM
omega2 = omega2*30/np.pi

#Plotando as varaveis de interesse
plt.figure(1)
plt.subplot(311) 
plt.plot(tempo,omega2,'r', label = "$L_a = 0 H$ e $b=0(N.m)/(rad/s)$")
plt.legend(fontsize=18)
plt.axes([0.45, 0.75, 0.3, 0.16])
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
erro1 = (omega1[0:3000] - omega[0:3000])
erro2 = (omega2[0:3000] - omega[0:3000])

# Definindo periodo de amostragem
T = tempo[1]-tempo[0]

# Definindo valores do IAE
IAE1 = np.trapz(abs(erro1), dx = T)
IAE2 = np.trapz(abs(erro2), dx = T)

# Definindo valores do ITAE
ITAE1 = np.trapz(abs(erro1)*tempo[0:3000], dx = T)
ITAE2 = np.trapz(abs(erro2)*tempo[0:3000], dx = T)
