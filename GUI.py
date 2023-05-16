import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import serial

def envois(data):
    # Fonction pour envoyer les données au périphérique connecté
    ser = serial.Serial(port="COM4", baudrate=9600, timeout=1)
    ser.write(bytes(str(data) + '\r\n', 'utf-8'))
    ser.flush()
    ser.close()

def update_distance_limit():
    # Fonction pour mettre à jour la limite de distance
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

def on_distance_limite_send(event):
    # Fonction appelée lors de l'envoi de la limite de distance
    on_distance_change(event)
    data = str(int(distance_var.get())) + "," + str(int(limite_var.get()))
    envois(data)

def on_distance_change(event):
    # Fonction appelée lors du changement de la distance
    distance = int(distance_scale.get())
    distance_var.set(distance)

# Création de la fenêtre principale
window = tk.Tk()
window.title("Interface de distance")
window.geometry("500x400")  # Taille de la fenêtre

distance_var = tk.IntVar(value=1)  # Variable pour stocker la valeur de distance
limite_var = tk.IntVar(value=250)  # Variable pour stocker la valeur de limite de distance

# Création des éléments de l'interface utilisateur
title_label = ttk.Label(window, text="Distance :", font=("Arial", 12, "bold"))
title_label.pack(pady=10)

distance_scale = ttk.Scale(window, from_=0, to=250, length=250, orient=tk.HORIZONTAL)
distance_scale.pack(pady=10)
distance_scale.set(100)

distance_limit_label = ttk.Label(window, text="Limite de distance :", font=("Arial", 12, "bold"))
distance_limit_label.pack()

distance_limit_entry = ttk.Entry(window)
distance_limit_entry.pack(pady=10)

update_button = ttk.Button(window, text="Mettre à jour", command=update_distance_limit)
update_button.pack(pady=10)

ttk.Label(window, text="Distance :", font=("Arial", 12, "bold")).pack()
distance_text_label = ttk.Label(window, textvariable=distance_var, font=("Arial", 14, "bold"))
distance_text_label.pack()

ttk.Label(window, text="Limite à ne pas dépasser :", font=("Arial", 12, "bold")).pack()
distance_text_label = ttk.Label(window, textvariable=limite_var, font=("Arial", 14, "bold"))
distance_text_label.pack()

distance_scale.bind("<B1-Motion>", on_distance_change)
distance_scale.bind("<ButtonRelease-1>", on_distance_limite_send)

window.mainloop()
