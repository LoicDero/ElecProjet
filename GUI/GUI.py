import serial
import time
import tkinter as tk
import threading

# Cette fonction va nous permettre d'injecter les données dans une variable partagées qui ensuite seront envoyées au pico
def enter_data_shared():
    """
    pre: entries has to be int
    post: insert of entries into shared_data, the first one is for
    minimal distance and the second one for maximal distance
    """
    val_min = entry_val_min.get()
    val_max = entry_val_max.get()
    shared_data['distance_max'] = int(val_max)
    shared_data['distance_min'] = int(val_min)

# Cette fonction nous permet de mettre a jour les données qui sont lu sur le pico
def update_label_mesured():
    """
    pre: -
    post: update de label for the mesured distance by the raspberry pi pico
    """
    label_mesured_distance.config(text="Distance mesurée : " + str(shared_data['mesurer']))
    window.after(100, update_label_mesured)

# Cette fonction nous permet d'écrire des données dans le stdin du pico et de lire les données envoyées par le pico
def send_and_read_data_to_pico():
    """
    pre: the right name for the serial connection have to be changed if needed
    post: send the data of the shared_data variable for the minimal distance and maximal distance,
    also read the stdout of the pico and store it into shared_data
    """
    ser = serial.Serial("/dev/cu.usbmodem141301", baudrate=9600, timeout=1)
    data = str(shared_data['distance_min'])+','+str(shared_data['distance_max'])+'\r\n'
    print(data)
    ser.write(bytes(data, 'utf-8'))
    #shared_data['mesurer'] = int(ser.readline().decode('utf-8'))
    ser.close()

# la boucle qui va lire les données du pico et les envoyées
def run_serial_loop():
    """
    pre: -
    post: call send_and_read_data_to_pico() and sleep for 0.1 second
    """
    while True:
        send_and_read_data_to_pico()
        time.sleep(0.1)

# les données de la variable partagées
shared_data = {'value': 0, 'mesurer': 0, 'distance_min': 20, 'distance_max': 40}

# création de la fenêtre pour notre interface graphique
window = tk.Tk()
window.title("Interface graphique")
window.minsize(400, 200)
window.maxsize(400, 200)

# création des labels et entries pour l'affichage des différents éléments qui doivent être présent dans notre interface
label_min = tk.Label(window, text="Valeur minimal : ")
label_min.pack()

entry_val_min = tk.Entry(window)
entry_val_min.pack()

label_max = tk.Label(window, text="Valeur maximal : ")
label_max.pack()
entry_val_max = tk.Entry(window)
entry_val_max.pack()

button = tk.Button(window, text="Changer les valeurs", command=enter_data_shared)
button.pack()

label_mesured_distance = tk.Label(window, text="Distance mesuré : " + str(shared_data['mesurer']))
label_mesured_distance.pack()
update_label_mesured()

# séparation en thread de l'interface graphique et de l'envoie et la lectures des données du pico
serial_thread = threading.Thread(target=run_serial_loop)
serial_thread.daemon = True
serial_thread.start()

# lancement de la boucle principale de notre interface graphique
window.mainloop()
