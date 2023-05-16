import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import serial

# Cette fonction va nous permettre d'injecter les données dans une variable partagées qui ensuite seront envoyées au pico
def envois(data):
    ser = serial.Serial(port="COM4", baudrate=9600, timeout=1)
    ser.write(bytes(str(data) + '\r\n', 'utf-8'))
    ser.flush()
    ser.close()

#
def update_distance_limit():
    limit = distance_limit_entry.get()
    try:
        limit = int(limit)
        if 1 <= limit <= 250:
            limite_var.set(limit)
        else:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Erreur", "Veuillez entrer une valeur numérique entière entre 1 et 250 pour la limite de distance.")

# Cette fonction nous permet de mettre a jour les données qui sont lu sur le pico
def on_distance_limite_send(event):
    on_distance_change(event)
    data = str(int(distance_var.get())) + "," + str(int(limite_var.get()))
    envois(data)

# Cette fonction nous permet d'écrire des données dans le stdin du pico et de lire les données envoyées par le pico
def on_distance_change(event):
    distance = int(distance_scale.get())  # Distance entière
    distance_var.set(distance)  # Mise à jour de la variable de distance

# Création de la fenêtre principale
window = tk.Tk()
window.title("Interface de distance")
window.minsize(400, 250)
window.maxsize(400, 250)

# Variable pour stocker la valeur de distance
distance_var = tk.IntVar(value=1)  # Initialisation à 1 centimetre
limite_var = tk.IntVar(value=250) # Initialisation à 1 centimetre

# Création des widgets
title_label = ttk.Label(window, text="Distance :")
title_label.pack()

distance_scale = ttk.Scale(window, from_=0, to=250,
                           length=250, orient=tk.HORIZONTAL)
distance_scale.pack()
distance_scale.set(100)  # Initialisation à 100 cm

distance_limit_label = ttk.Label(window, text="Limite de distance:")
distance_limit_label.pack()

distance_limit_entry = ttk.Entry(window)
distance_limit_entry.pack()

update_button = ttk.Button(
    window, text="Mettre à jour", command=update_distance_limit)
update_button.pack()

distance_gauge = ttk.Progressbar(
    window, variable=distance_var, mode="determinate", maximum=250)
distance_gauge.pack()
distance_var.set(100)  # Initialisation à 1 mètre

ttk.Label(window, text="Distance :").pack()
distance_text_label = ttk.Label(
    window, textvariable=distance_var, font=("Arial", 14, "bold"))
distance_text_label.pack()

ttk.Label(window, text="Limite à ne pas dépasser :").pack()
distance_text_label = ttk.Label(
    window, textvariable=limite_var, font=("Arial", 14, "bold"))
distance_text_label.pack()

# Appel de la fonction on_distance_change lorsque la jauge est déplacée
distance_scale.bind("<B1-Motion>", on_distance_change)
distance_scale.bind("<ButtonRelease-1>", on_distance_limite_send)

# Exécution de la boucle principale
window.mainloop()
