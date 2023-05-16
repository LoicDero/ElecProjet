import machine
from machine import Pin, Timer, ADC
import _thread
import utime
import sys
import select


# dans cette fonction on va initialiser les pins de notre sonde HCSR04
def init_hcsr04():
    """
    pre: the numbers in Pin() function has to be changed with your connection GP
    post: initialize the pins of the HCSR04
    """
    global trigger
    global echo
    
    trigger =  Pin(28, Pin.OUT, pull=None)
    trigger.value(0)
    echo = Pin(22, Pin.IN, pull=None)
        
        
# dans cette fonction on initialise les pins de nos 7 segments et des pins qui vont envoyées des données a notre décodeurs
def init_decodeur():
    """
    pre: the numbers in Pin() function has to be changed with your connection GP
    post: initialize the pins who will be used to send data into the decoder and the two Seven-segment display
    """
    global Pin_SEG1
    global Pin_SEG2
    global Pin_LE_1
    global Pin_LE_2
    global Pin_LE_4
    global Pin_LE_8
    global Dot_point
    
    Pin_LE_1 = Pin(10, Pin.OUT)
    Pin_LE_2 = Pin(13, Pin.OUT)
    Pin_LE_4 = Pin(12, Pin.OUT)
    Pin_LE_8 = Pin(11, Pin.OUT)
    Pin_SEG1 = Pin(18, Pin.OUT)
    Pin_SEG2 = Pin(19, Pin.OUT)
    Dot_point = Pin(2, Pin.OUT)
    
    Pin_SEG1.value(0)
    Pin_SEG2.value(0)
    Dot_point.value(1)
    
    Pin_LE_1.value(0)
    Pin_LE_2.value(0)
    Pin_LE_4.value(0)
    Pin_LE_8.value(0)
    
    
# dans cette fonction on va initialiser les pins de nos leds
def init_led():
    """
    pre: the numbers in Pin() function has to be changed with your connection GP
    post: initialize the pins of the leds
    """
    global LED_rouge
    global LED_verte
    
    LED_rouge = Pin(1, Pin.OUT)
    LED_verte = Pin(0, Pin.OUT)
    LED_rouge.value(0)
    LED_verte.value(0)
    
    
# dans cette fonction on envoie une liste d'éléments qui vont être être injecter a notre décodeurs
def number_dec(tab):
    """
    pre: tab has to be a list with the values 0 or 1
    post: send 0 or 1 into the decoder
    """
    Pin_LE_8.value(int(tab[0]))
    Pin_LE_4.value(int(tab[1]))
    Pin_LE_2.value(int(tab[2]))
    Pin_LE_1.value(int(tab[3]))
    
    
# dans cette fonction on va envoyé une impulsion et la transformer en distance par cm
def send_pulsation(shared_data):
    """
    pre: the shared_data variable
    post: mesure the distance of the HCSR04 and convert it into cm, after it is stored into
    the shared_data
    """
    utime.sleep_us(1)
    trigger.value(1)
    utime.sleep_us(1)
    trigger.value(0)
    pulse = ((machine.time_pulse_us(echo, 1)) / 2) / 29.1
    with shared_data['lock']:
        shared_data['pulsation'] = int(pulse)


# envoie retourne une liste de valeur de la mesure dont le premier éléments et la dizaine et le 2ème et l'unité
def convert_pulse(param):
    """
    pre: param has to be decimal value
    post: return the decimal value into list with result_number[0] is the ten and result_number[1] is the unit
    """
    valeur1=int(param/10)
    valeur2=param%10
    result_numbers=[valeur1,valeur2]
    return result_numbers


# dans cette fonction on traduit en binaire un nombre décimal
def convert_binary(nbr):
    """
    pre: nbr has to be a int
    post: return a list who is the binary version of a number --> 1 == ['0','0','0','1']
    """
    res=bin(nbr)[2::]
    tab=list(res)
    while len(tab)<4:
        tab.insert(0,str("0"))
    return tab


# cette fonction nous permet d'allumer la led rouge ou verte en fonction de si la distance est respecté  
def activation_led(distance_mesurer, distance_max, distance_min):
    """
    pre: parameters has to be integers
    post: if 1 parameters is between max distance and min distance the green led is lighted
    else the red one is blinking
    """
    if distance_mesurer > distance_max or distance_mesurer < distance_min:
        LED_rouge.value(1)
        LED_verte.value(0)
        print('false')
    else:
        LED_verte.value(1)
        LED_rouge.value(0)
        print('true')
        
        
# cette fonction va transformer un chiffre decimal a 3 chiffres en 2 chiffres et allumera le dot point
# ex : 152 devient 1.5
def activation_dot_point(decimal_pulsation):
    """
    pre: parameter has to be int
    post: change if a number is 3 digit it change to 2 digit and display
    the 7 segment with a dot point
    """
    if decimal_pulsation[0] > 9:
        dizaine = int(str(decimal_pulsation[0])[0])
        unite = int(str(decimal_pulsation[0])[1])
        decimal_pulsation[0] = dizaine
        decimal_pulsation[1] = unite
        Dot_point.value(0)
    else:
        Dot_point.value(1)
        
        
# on appel nos fonction qui initialise nos différents composant
init_decodeur()
init_hcsr04()
init_led()

poll_object = select.poll()
poll_object.register(sys.stdin, 1)


# dans cette fonction on va lire ce qui nous sera transmis par notre ordinateur dans le stdin
def read_stdin():
    """
    pre: the data has to be bytes send like this --> b'12,34\r\n', the first value is
    the minimal distance and second is maximal distance
    post: read data from the stdin and store it into shared_data
    """
    if poll_object.poll(0):
        line = sys.stdin.buffer.readline()
        if line:
            received_data = line.decode('utf-8')
            data_parts = received_data.split(',')
            if len(data_parts) == 2:
                try:
                    shared_data['distance_min'] = int(data_parts[0])
                    print(int(data_parts[0]))
                    shared_data['distance_max'] = int(data_parts[1])
                    print(int(data_parts[1]))
                except ValueError:
                    print("Erreur de conversion des données en entiers")


# dans cette fonction on va initialiser la boucle pour notre thread qui mesurera la distance
def hcsr_thread(shared_data):
    """
    pre: -
    post: call send_pulsation()
    """
    while True:
        send_pulsation(shared_data)
        utime.sleep_ms(300)


def main_thread(shared_data):
    segment_toggle = False
    while True:
        with shared_data['lock']:
            pulsation = shared_data['pulsation']
            read_stdin()
            #print(shared_data['distance_max'], shared_data['distance_min'])
            activation_led(pulsation, shared_data['distance_max'], shared_data['distance_min'])
            #print(pulsation)
            decimal_pulsation = convert_pulse(pulsation)
            activation_dot_point(decimal_pulsation)

            if segment_toggle:
                Pin_SEG1.value(1)
                tab = convert_binary(decimal_pulsation[1])
                
            else:
                Pin_SEG2.value(1)
                tab = convert_binary(decimal_pulsation[0])

        segment_toggle = not segment_toggle
        utime.sleep_ms(1000)
        number_dec(tab)
        Pin_SEG2.value(0)
        Pin_SEG1.value(0)


# la variable partagées pour nos différents composant
shared_data = {'pulsation': 0, 'lock': _thread.allocate_lock(), 'distance_min': 20, 'distance_max':40}

# la séparation en thread de la fonction main et hcsr_thread
hcsr_thread_obj = _thread.start_new_thread(hcsr_thread, (shared_data,))
main_thread(shared_data)


