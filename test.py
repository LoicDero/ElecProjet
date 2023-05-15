import machine
import time

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
Afficheur_Dixaines = [
    machine.Pin(8, machine.Pin.OUT),
    machine.Pin(9, machine.Pin.OUT),
    machine.Pin(10, machine.Pin.OUT),
    machine.Pin(11, machine.Pin.OUT),
    machine.Pin(12, machine.Pin.OUT),
    machine.Pin(13, machine.Pin.OUT),
    machine.Pin(14, machine.Pin.OUT)
]

Afficheur_Unitees = [
    machine.Pin(16, machine.Pin.OUT),
    machine.Pin(20, machine.Pin.OUT),
    machine.Pin(21, machine.Pin.OUT),
    machine.Pin(22, machine.Pin.OUT),
    machine.Pin(26, machine.Pin.OUT),
    machine.Pin(27, machine.Pin.OUT),
    machine.Pin(28, machine.Pin.OUT)
]

# Fonction pour allumer un segment donné


def allumer_segment(segment):
    segment.off()

# Fonction pour éteindre un segment donné


def eteindre_segment(segment):
    segment.on()


# Boucle principale pour allumer et éteindre chaque segment à tour de rôle
while True:
    for segment in Afficheur_Dixaines:
        eteindre_segment(segment)

    for segment in Afficheur_Unitees:
        eteindre_segment(segment)

    for segment in Afficheur_Dixaines:
        allumer_segment(segment)
        time.sleep(0.2)
        eteindre_segment(segment)
        time.sleep(0.2)

    for segment in Afficheur_Unitees:
        allumer_segment(segment)
        time.sleep(0.2)
        eteindre_segment(segment)
        time.sleep(0.2)
