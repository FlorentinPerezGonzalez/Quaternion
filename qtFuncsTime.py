from math import *
import numpy as np
import quaternion
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from functools import reduce
from decTime import temporizadorGetTime, temporizador
import sys

def ramal(I, prev=[], base=0):
    # Convierte el robot a una secuencia de puntos para representar
    O = []
    if I:
        if isinstance(I[0][0], list):
            for j in range(len(I[0])):
                O.extend(ramal(I[0][j], prev, base or j < len(I[0])-1))
        else:
            O = [I[0]]
            O.extend(ramal(I[1:], I[0], base))
            if base:
                O.append(prev)
    return O


def muestra_robot(O, ef=[]):
    # Pinta en 3D
    OR = ramal(O)
    OT = np.array(OR).T
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Bounding box cúbico para simular el ratio de aspecto correcto
    max_range = np.array([OT[0].max()-OT[0].min(), OT[1].max()-OT[1].min(), OT[2].max()-OT[2].min()
                          ]).max()
    Xb = (0.5*max_range*np.mgrid[-1:2:2, -1:2:2, -1:2:2][0].flatten()
          + 0.5*(OT[0].max()+OT[0].min()))
    Yb = (0.5*max_range*np.mgrid[-1:2:2, -1:2:2, -1:2:2][1].flatten()
          + 0.5*(OT[1].max()+OT[1].min()))
    Zb = (0.5*max_range*np.mgrid[-1:2:2, -1:2:2, -1:2:2][2].flatten()
          + 0.5*(OT[2].max()+OT[2].min()))
    for xb, yb, zb in zip(Xb, Yb, Zb):
        ax.plot([xb], [yb], [zb], 'w')
    ax.plot3D(OT[0], OT[1], OT[2], marker='s')
    ax.plot3D([0], [0], [0], marker='o', color='k', ms=10)
    if not ef:
        ef = OR[-1]
    ax.plot3D([ef[0]], [ef[1]], [ef[2]], marker='s', color='r')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
    return

def cuaternion_rotacion(n, theta):
    # n es un vector
    # theta es un angulo
    w = cos(theta/2)
    x = n[0]*sin(theta/2)
    y = n[1]*sin(theta/2)
    z = n[2]*sin(theta/2)
    return(np.quaternion(w, x, y, z))

def cuaternion_rotacionList(art_list):
    # Crea un cuaternion a partir de una lista de forma [x, y, z, angulo]
    th = art_list[3] * pi/180
    w = cos(th/2)
    x = art_list[0]*sin(th/2)
    y = art_list[1]*sin(th/2)
    z = art_list[2]*sin(th/2)
    return(np.quaternion(w, x, y, z))

# Calcula el tiempo de calcular X brazos con quaterniones
@temporizador
def directKinematicsQt(arms, articulations): 
    # Los brazos no pueden tener tamaño negativo
    if len(arms) <= 0 or len(articulations) <= 0:
        raise Exception('La cantidad de articulaciones no puede ser 0 o menos')
    # Crear cuaterniones en base al tamaño de los brazos
    arms_quaternions = [np.quaternion(0, size, 0, 0) for size in arms]
    # Crear cuaterniones en base a las rotaciones introducidas por el usuario
    quaternions_rotation_list = [cuaternion_rotacionList(articulation) for articulation in articulations]
    # Crear los quaterniones conjugados de los anterioes
    quaternions_rotation_list_conjugate = [np.conjugate(qt) for qt in quaternions_rotation_list]
    points_list = [] # Lista de puntos una vez aplicada la rotación
    # Guardamos el valor de la izquierda de r en la fórmula para ahorrar operaciones
    qt_memorization = quaternions_rotation_list[0]
    qt_memorizationC = quaternions_rotation_list_conjugate[0]
    # Inclusión del primer punto en la lista
    points_list.append(qt_memorization * arms_quaternions[0] * quaternions_rotation_list_conjugate[0])
    # Bucle que realiza la fórmula para obtener el valor de los puntos siguientes
    for i in range(1, len(arms)):
        qt_memorization *= quaternions_rotation_list[i]
        inicio = qt_memorization * arms_quaternions[i]
        # conjugate_multiplication = reduce(lambda a,b : a * b, [inicio] + quaternions_rotation_list_conjugate[::-1][:i+1])
        qt_memorizationC = quaternions_rotation_list_conjugate[i] * qt_memorizationC
        conjugate_multiplication = inicio * qt_memorizationC
        points_list.append(conjugate_multiplication + points_list[i - 1])
    # Creamos una nueva lista que representa las posiciones de los puntos en 3 dimensiones
    points_3d = [[0, 0, 0, 1]] + list(map(lambda x: [x.x, x.y, x.z, 1], points_list))
    # print(points_3d)
    # muestra_robot(points_3d) # Lanza el gráfico interactivo que muuestra el brazo
    
nvar=2 # Número de variables
if len(sys.argv) != nvar:
    sys.exit('El número de articulaciones no es el correcto ('+str(nvar)+')')
pp=int(sys.argv[1])

armsX = [5] * pp
articulationsX = [[0, 0, 1, 45]] * pp

directKinematicsQt(armsX, articulationsX)