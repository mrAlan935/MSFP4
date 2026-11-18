"""
Práctica 4: Sistema endocrino

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Obregon Maldonado Alan Yahir
Número de control: 23212221
Correo institucional: l23212221@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx

"""
import numpy as np
import math as m
import control as ctrl
import matplotlib.pyplot as plt

# Datos generales de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,10,5
N = round(tend/dt) + 1
t = np.linspace(t0,tend,N)
u = np.ones(N)

def sis(C, R2, nombre):
    R1, L = 1E3,100E-3
    num = [L, R2]
    den = [C*L*R1,C*R1*R2+L,R1+R2]
    sys = ctrl.tf(num, den)
    print(f"Función de transferencia {nombre}: {sys}\n")
    return sys

sysControl = sis(1E-6, 100E3, "Control")
sysCaso = sis(1000E-6, 1E3,"Caso")

# Componentes del controlador
kP,kI,kD = 33354.2821859582,206021749.697766,0.181162854040385
Cr = 1E-6
Re = 1/(Cr*kI)
Rr = kP*Re
Ce = kD/Rr
numPID = [Re*Rr*Ce*Cr,Re*Ce+Rr*Cr,1]
denPID = [Re*Cr,0]
PID = ctrl.tf(numPID,denPID)

# Sistema de control en lazo cerrado
sysPID = ctrl.feedback(ctrl.series(PID,sysCaso),1,sign = -1)
print(f"Función de transferencia en lazo cerrado: {sysPID}\n")

#Colores
clr1 = np.array([97,45,83])/255
clr2 = np.array([255,190,145])/255
clr3 = np.array([44,87,69])/255
clr4 = np.array([45,100,200])/255

# Funciones del sistema en lazo abierto y lazo cerrado
def openloop(t,sys,u):
    _,Vs = ctrl.forced_response(sys,t,u,x0)
    return Vs

def closedloop(t,sys,u):
    _,tratamientoPID = ctrl.forced_response(sys,t,u,x0)
    return tratamientoPID

#Respuestas: Simulaciones numéricas
Control = openloop(t,sysControl,u)
Caso = openloop(t,sysCaso,u)
Tratamiento = closedloop(t,sysPID,Control)
fg = plt.figure()
fg.set_size_inches(w,h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.plot(t,u,'-',linewidth=1.5,color=clr1,label='Ve(t)')
plt.plot(t,Control,'-',linewidth=1.5,color=clr2,label='Vs(t): Control')
plt.plot(t,Caso,'-',linewidth=1.5,color=clr3,label='Vs(t): Caso')
plt.plot(t,Tratamiento,'--',linewidth=1.5,color=clr4,label='PID(t)')
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.1,1.2); plt.yticks(np.arange(-0.1,1.3,0.1))
plt.xlabel('t [s]')
plt.ylabel('Ve(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=4,frameon=False)
plt.show()
fg.savefig('Control_caso_python4.pdf',bbox_inches='tight')