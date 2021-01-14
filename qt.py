from math import *
from tkinter import *
from tkinter.font import Font
import numpy as np
import quaternion
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

arms_frame = 0
all_arms = []
arts_frame = 0
all_arts = []

class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self, height=200)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

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

def generate_scrolls():
  global arms_frame, arts_frame
  n_arts = arms_entry.get()
  arms_frame = ScrollableFrame(root)
  arts_frame = ScrollableFrame(root)
  arms_frame.pack(pady=5, anchor="w", fill="x")
  arts_frame.pack(pady=1, anchor="w", fill="x")
  generate_arms_scrolls(n_arts)
  generate_arts_scrolls(n_arts)

def generate_single_arm(counter):
  global arms_frame, all_arms
  Label(arms_frame.scrollable_frame, text=f"Brazo {counter + 1} - Longitud", font=8).grid(row=counter, column=0, pady=3, padx=(0, 30))
  aux = Entry(arms_frame.scrollable_frame, width=8, justify="right")
  aux.insert(0, 0)
  aux.grid(row=counter, column=1, padx=(0, 10))
  all_arms.append(aux)

def generate_single_art(counter):
  global arts_frame, all_arts
  all_arts.append([])
  axis = ["X", "Y", "Z"]
  col = 1
  Label(arts_frame.scrollable_frame, text=f"Art. {counter + 1}", font=8).grid(row=counter, column=0, pady=3, padx=(0, 30))
  for coordinate in axis:
    Label(arts_frame.scrollable_frame, text=f"{coordinate}: ", font=10).grid(row=counter, column=col, pady=3)
    aux = Entry(arts_frame.scrollable_frame, width=4, justify="right")
    aux.insert(0, 0)
    aux.grid(row=counter, column=col + 1, padx=(0, 10))
    all_arts[-1].append(aux)
    col += 2
  Label(arts_frame.scrollable_frame, text="Ángulo", font=10).grid(row=counter, column=col, pady=3)
  aux = Entry(arts_frame.scrollable_frame, width=4, justify="right")
  aux.insert(0, 0)
  aux.grid(row=counter, column=col + 1, padx=(0, 10))
  all_arts[-1].append(aux)

def generate_arms_scrolls(number):
  for i in range(int(number) + 1):
    generate_single_arm(i)

def generate_arts_scrolls(number):
  for i in range(int(number)):
    generate_single_art(i)

# Parte gráfica

root = Tk()
root.title("CD con quaterniones")
root.geometry("500x500")
root.resizable(False, False)
main_frame = Frame(root)
main_frame.pack(side="top")
main_frame.pack_propagate(False)
Label(main_frame, text="Articulaciones", font=Font(family='Arial', size=14)).grid(row=0, column=0, sticky="w")
arms_entry = Spinbox(main_frame, from_=0, to=10, format="%1.0f", wrap=True,
            font=Font(family='Arial', size=14), increment=1, width=10)
arms_entry.grid(row=0, column=1, sticky="e", padx=(10,10))
Button(main_frame, text="Enviar", pady=1, height=1, cursor="hand2", command=generate_scrolls).grid(row=0, column=2)

root.mainloop()

# cuaterniones de desplazamiento
r1 = np.quaternion(0, 5, 0, 0)
r2 = np.quaternion(0, 5, 0, 0)

# vectores de rotaci�n
n1 = [1, 0, 0]
n2 = [0, 1, 0]

# introducci�n de las variables articulares
print('')
t1 = float(input('valor de theta1 en grados  '))
t1 = t1*pi/180
t2 = float(input('valor de theta2 en grados  '))
t2 = t2*pi/180

# calculo de los cuaterniones de rotaci�n
q1 = cuaternion_rotacion(n1, t1)
q1c = np.conjugate(q1)

q2 = cuaternion_rotacion(n2, t2)
q2c = np.conjugate(q2)


# calculo del punto o1
i1 = q1 * r1
o1 = i1 * q1c


# calculo del punto o2
i2 = q1 * q2
i2 = i2 * r2
i2 = i2 * q2c
i2 = i2 * q1c
o2 = o1 + i2


# impresi�n de los resultados
print('')
print('punto uno del robot')
print(o1)
print('')
print('punto dos del robot')
print(o2)

print(quaternion.as_float_array(o1))

muestra_robot([[0, 0, 0, 1], [o1.x, o1.y, o1.z, 1], [o2.x, o2.y, o2.z, 1]])
input()
