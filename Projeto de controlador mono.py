import numpy as np # Importando a biblioteca Numpy
import control as ct # Importando a biblioteca Control
import matplotlib.pyplot as plt # Importando a bi0blioteca Matplotlib.pyplot

plt.close('all') # Fecha gráficos
s = ct.tf('s') # Criando uma função de transferência de F(s) = s
"""
Defininido o modelo do sistema

         1
G = -----------
     Lf*s + Rf
"""
Lf = 21.3
Rf = 212.94
G = ct.tf([1],[Lf, Rf]); # Defininido o modelo do sistema
#%%
"""
Especificações de Desempenho
"""
# Deseja-se malha fechada com tempo de acomodação de 1s, sobressinal de no máximo 10% e menor tempo de subida possível.
# Para menor tempo de subida, parte imaginária deve ser a maior possível.
# Logo, tomando o sobressinal de 10%, calculando do zeta e wn:

OS = 0.1 # Sobressinal maximo
ts = 0.8 # Tempo de acomodação
zeta = -np.log(OS)/np.sqrt(np.pi**2+np.log(OS)**2) # Amortecimento desejado
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
ct.root_locus(G/s)
plt.title('Sistema G(s) com 1 polo a mais na origem')
plt.plot(np.real(p1), np.imag(p1),'g*')
plt.plot(np.real(p2), np.imag(p2),'g*', label = 'Polos desejados')
plt.legend()

# Ciando o controlador 
CL = (1524)/(s)

# Criando a malha fechada
Mf = ct.minreal(ct.feedback(CL*G))