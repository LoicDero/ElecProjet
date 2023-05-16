import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def update_distance_limit():
    limit = distance_limit_entry.get()
    try:
        limit = float(limit)
        distance_limit.set(limit)
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer une valeur numérique pour la limite de distance.")


def on_distance_change(event):
    distance = round(distance_scale.get(),1)  # Distance arrondie à l'unité (centimètres)
    distance_var.set(distance)  # Mise à jour de la variable de distance
    distance_text_label.config(text=f"{distance:.1f}")  # Mise à jour du texte de la distance

# Création de la fenêtre principale
window = tk.Tk()
window.title("Interface de distance")
window.minsize(400, 250)
window.maxsize(400, 250)

# Variable pour stocker la valeur de distance
distance_var = tk.IntVar(value=1.0)  # Initialisation à 1 mètre

# Création des widgets
title_label = ttk.Label(window, text="Distance :")
title_label.pack()

distance_scale = ttk.Scale(window, from_=0, to=250, length=250, orient=tk.HORIZONTAL, variable=distance_var)
distance_scale.pack()
distance_scale.set(100)  # Initialisation à 100 cm

distance_limit_label = ttk.Label(window, text="Limite de distance:")
distance_limit_label.pack()

distance_limit_entry = ttk.Entry(window)
distance_limit_entry.pack()

update_button = ttk.Button(window, text="Mettre à jour", command=update_distance_limit)
update_button.pack()

distance_gauge = ttk.Progressbar(window, variable=distance_var, mode="determinate", maximum=250)
distance_gauge.pack()
distance_var.set(100)  # Initialisation à 1 mètre

ttk.Label(window, text="Distance :").pack()
distance_text_label = ttk.Label(window, textvariable=distance_var, font=("Arial", 14, "bold"))
distance_text_label.pack()


# Appel de la fonction on_distance_change lorsque la jauge est déplacée
distance_scale.bind("<B1-Motion>", on_distance_change)

# Exécution de la boucle principale
window.mainloop()
