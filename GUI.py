import serial
import time
import tkinter as tk
import threading


def print_text()


value = entry.get()
shared_data['value'] = int(value)
print(Texte saisi, value)


def send_data_to_pico()


pico_port = devcu.usbmodem141301
ser = serial.Serial(pico_port, baudrate=11400, timeout=1)
data = str(shared_data['distance_min'])+',' + \
    str(shared_data['distance_max'])
test = ser.write(b'10,50')
print(test)
ser.close()


def run_serial_loop()


while True
send_data_to_pico()
time.sleep(1)


shared_data = {'value' 0, 'mesurer' 0, 'distance_min' 70, 'distance_max' 80}

# Créer la fenêtre principale
window = tk.Tk()
window.title(Interface graphique)

# Définir la taille de la fenêtre
window.minsize(400, 200)
window.maxsize(400, 200)

# Créer le champ d'entrée de texte
entry = tk.Entry(window)
entry.pack()

# Créer le bouton
button = tk.Button(window, text=Entrez, command=print_text)
button.pack()

label_value = tk.Label(window, text=Valeur)
label_value.pack()

# Créer et démarrer le thread pour la boucle série
serial_thread = threading.Thread(target=run_serial_loop)
# Terminer le thread lorsque le thread principal se termine
serial_thread.daemon = True
serial_thread.start()

# Démarrer la boucle principale de l'interface graphique
window.mainloop()
