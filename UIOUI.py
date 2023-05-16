import machine
import utime
import time
import sys
import select


poller = select.poll()
poller.register(sys.stdin, 1)

alarm = 250
distance = 99

# Fonction pour mesurer la distance avec la sonde HC-SR04
def read_from_port():
    if poller.poll(0):
        line = sys.stdin.buffer.readline()
        if line:
            data = line.decode('utf-8')
            return data

# Fonction pour mesurer la distance avec la sonde HC-SR04
def dechiffre():
    global distance
    global alarm
  
    data = read_from_port()
    if data != None:
        data_Array = data.split(',')
        distance = int(data_Array[0])
        alarm = int(data_Array[1])

def alarme():
    red_led.on()
    green_led.off()

# Définition des chiffres à afficher (en binaire)
digit_patterns = {
    0: [0, 0, 0, 0, 0, 0, 1],
    1: [1, 0, 0, 1, 1, 1, 1],
    2: [0, 0, 1, 0, 0, 1, 0],
    3: [0, 0, 0, 0, 1, 1, 0],
    4: [1, 0, 0, 1, 1, 0, 0],
    5: [0, 1, 0, 0, 1, 0, 0],
    6: [0, 1, 0, 0, 0, 0, 0],
    7: [0, 0, 0, 1, 1, 1, 1],
    8: [0, 0, 0, 0, 0, 0, 0],
    9: [0, 0, 0, 0, 1, 0, 0]
}

# Définition des broches pour les deux afficheurs 7 segments
afficheur_Dixaines = []
afficheur_Unitees = []

segment_0 = machine.Pin(8, machine.Pin.OUT)
segment_1 = machine.Pin(9, machine.Pin.OUT)
segment_2 = machine.Pin(10, machine.Pin.OUT)
segment_3 = machine.Pin(11, machine.Pin.OUT)
segment_4 = machine.Pin(12, machine.Pin.OUT)
segment_5 = machine.Pin(13, machine.Pin.OUT)
segment_6 = machine.Pin(14, machine.Pin.OUT)

afficheur_Dixaines = [segment_0, segment_1, segment_2,
                      segment_3, segment_4, segment_5, segment_6]

segment_0 = machine.Pin(16, machine.Pin.OUT)
segment_1 = machine.Pin(20, machine.Pin.OUT)
segment_2 = machine.Pin(21, machine.Pin.OUT)
segment_3 = machine.Pin(22, machine.Pin.OUT)
segment_4 = machine.Pin(26, machine.Pin.OUT)
segment_5 = machine.Pin(27, machine.Pin.OUT)
segment_6 = machine.Pin(28, machine.Pin.OUT)

afficheur_Unitees = [segment_0, segment_1, segment_2,
                     segment_3, segment_4, segment_5, segment_6]


# Définition du la broche pour le point
dot_point = machine.Pin(5, machine.Pin.OUT)

# Définition des broches pour les leds
green_led = machine.Pin(1, machine.Pin.OUT)
red_led = machine.Pin(0, machine.Pin.OUT)

red_led.off()
green_led.on()

# Définition de la broche pour la sonde HC-SR04
trigger = machine.Pin(18, machine.Pin.OUT)
echo = machine.Pin(19, machine.Pin.IN)

# Fonction pour afficher un chiffre sur un afficheur 7 segments
def afficher_chiffre(digit, segments):
    digit = int(digit)

    for i in range(len(segments)):
        if digit_patterns[digit][i]:
            segments[i].on()
        else:
            segments[i].off()


# Boucle principale pour mesurer la distance et afficher les deux premiers chiffres
while True:
    # Mesure la distance
    dechiffre()

    if distance > alarm:
        alarme()
    else:
        red_led.off()
        green_led.on()


    segment_0.on()
    if distance > 99:
        dot_point.off()

    else:
        dot_point.on()

    dist = str(distance)

    # Récupère les deux premiers chiffres de la distance
    if distance < 10:
        for segment in afficheur_Dixaines:
            segment.on()
        second_digit = dist[0]
        afficher_chiffre(second_digit, afficheur_Unitees)
    else :
        first_digit = dist[0]
        second_digit = dist[1]
        afficher_chiffre(first_digit, afficheur_Dixaines)
        afficher_chiffre(second_digit, afficheur_Unitees)

    # # Attend une seconde avant de mesurer à nouveau
    utime.sleep(0.5)
