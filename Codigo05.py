import numpy as np # Importando a biblioteca Numpy
import control as ct # Importando a biblioteca Control
import matplotlib.pyplot as plt # Importando a bi0blioteca Matplotlib.pyplot

plt.close('all') # Fecha gráficos
s = ct.tf('s') # Criando uma função de transferência de F(s) = s
"""
Defininido o modelo do sistema
"""
G = (6.5*10**(-10)*s + 4.576*10**(-3))/(1.638*10**(-11)*s**2 + 1.153*10**(-4)*s + 0.442) 
#%%
"""
Especificações de Desempenho
"""
# Deseja-se malha fechada com tempo de acomodação de 1s, sobressinal de no máximo 10% e menor tempo de subida possível.
# Para menor tempo de subida, parte imaginária deve ser a maior possível.
# Logo, tomando o sobressinal de 10%, calculando do zeta e wn:

OS = 0.1 # Sobressinal maximo
ts = 0.8 # Tempo de acomodação
zeta = -np.log(OS)/np.sqrt(np.pi**2+np.log(OS)**2); # Amortecimento desejado
wn = 4/(zeta*ts) # wn necessario [ts = 4/(zeta*wn)]
#%%
"""
Aplicando a técnica
"""
# Polos do sistema de segunda ordem equivalente às especificações
p1 = -zeta*wn + wn*np.sqrt(1-zeta**2)*1j # Definindo o primeiro polo
p2 = np.conj(p1) # Definindo o segundo polo

# =======================
# Aplicando LGR
# =======================

# Determinando os polos e zeros do sistema
polos = ct.pole(G)
zeros = ct.zero(G)

# Observando o Lugar Geométrico das Raízes
plt.figure()
ct.root_locus(G)
plt.plot(np.real(p1), np.imag(p1),'g*')
plt.plot(np.real(p2), np.imag(p2),'g*', label = 'Polos desejados')
plt.legend()
plt.grid()

CL = 1/(s*(s+10))

plt.figure()
ct.root_locus(ct.minreal(G*CL))
plt.plot(np.real(p1), np.imag(p1),'r', marker = 'X', markersize = 18)
plt.plot(np.real(p2), np.imag(p2),'r', marker = 'X', markersize = 18, label = 'Polos desejados')
plt.plot(-10, 0,'b', marker = 'X', markersize = 18)
plt.plot(0, 0,'b', marker = 'X', markersize = 18, label = 'Polos do controlador')
plt.legend(fontsize = 18)
plt.grid()
plt.xlim([-12,0])
plt.ylim([-10,10])
plt.xlabel('Parte Real', fontsize=18)
plt.ylabel('Parte Imaginária', fontsize=18)

CL = 6901*CL
