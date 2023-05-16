import machine
import utime
import time
import sys
import select


poller = select.poll()
poller.register(sys.stdin,1)



distance = 99

def read_from_port():
    usb = machine.pyb.USB_VCP()
    usb.init()
    if usb.any():
        line = usb.readline()   
        usb.close()
    if line:
        return (int)(line.decode('utf-8'))
    else:
        usb.close()
        

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
green_led.off()

# Définition de la broche pour la sonde HC-SR04
trigger = machine.Pin(18, machine.Pin.OUT)
echo = machine.Pin(19, machine.Pin.IN)


# Fonction pour mesurer la distance avec la sonde HC-SR04
def get_distance():
    reading = read_from_port()
    if reading != None:
        global distance
        distance = reading


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
    
    get_distance()

    segment_0.on()
    if distance > 99:
        dot_point.off()

        # red_led.on()
        # green_led.off()
    else:
        dot_point.on()

        # green_led.on()
        # red_led.off()

    dist = str(distance)

    # Récupère les deux premiers chiffres de la distance
    first_digit = dist[0]
    second_digit = dist[1]

    # Affiche les chiffres sur les deux afficheurs 7 segments
    afficher_chiffre(first_digit, afficheur_Dixaines)
    afficher_chiffre(second_digit, afficheur_Unitees)

    # # Attend une seconde avant de mesurer à nouveau
    utime.sleep(0.5)