from math import *
import numpy as np
from numpy.lib.polynomial import roots
import quaternion
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tkinter import *
from tkinter.font import Font
from qtFuncs import directKinematicsQt


arms_frame = 0
all_arms = []
arts_frame = 0
send_button = 0
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


def button_kinematics():
    global all_arms, all_arts
    all_arms2 = list(map(lambda x: float(x.get()), all_arms))
    all_arts2 = []
    for art in all_arts:
        all_arts2.append(list(map(lambda x: float(x.get()), art)))
    directKinematicsQt(all_arms2, all_arts2)

def generate_scrolls():
  global arms_frame, arts_frame, all_arms, all_arts, send_button
  n_arts = arms_entry.get()
  all_arms = []
  all_arts = []
  aux = False
  if (arms_frame):
    arms_frame.destroy()
    arts_frame.destroy()
    aux = True
  arms_frame = ScrollableFrame(root)
  arts_frame = ScrollableFrame(root)
  arms_frame.pack(pady=5, anchor="w", fill="x")
  arts_frame.pack(pady=1, anchor="w", fill="x")
  generate_arms_scrolls(n_arts)
  generate_arts_scrolls(n_arts)
  if (send_button):
    send_button.destroy()
  send_button = Button(root, text="Enviar", pady=1, height=1, cursor="hand2", command=button_kinematics)
  send_button.pack()

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
  for i in range(int(number)):
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
