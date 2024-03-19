from machine import UART, Pin, PWM, 
import utime,time,_thread
modulo = UART(0, 9600, tx=Pin(16), rx=Pin(17))
""" Pines usados para el ultrasondo,motores,leds y buzzer
"""
trig = Pin(7, Pin.OUT)
echo = Pin(8, Pin.IN)
motora1 = Pin(18, Pin.OUT)
motora2 = Pin(19, Pin.OUT)
motorb1 = Pin(20, Pin.OUT)
motorb2 = Pin(21, Pin.OUT)
blancas = Pin(6, Pin.OUT)
verdes =  Pin(27, Pin.OUT)
rojas = Pin(26, Pin.OUT)
BUZZER_PIN = 22 
buzzer = PWM(Pin(BUZZER_PIN, Pin.OUT))
# funciones que son llamadas en el while Tru:
def adelante():
    motora1.high()
    motora2.low()
    motorb1.low()
    motorb2.high()

def atras():
    motora1.low()
    motora2.high()
    motorb1.high()
    motorb2.low()

def izquierda():
    motora1.low()
    motora2.high()
    motorb1.low()
    motorb2.high()

def derecha():
    motora1.high()
    motora2.low()
    motorb1.high()
    motorb2.low()

def parar():
    motora1.low()
    motora2.low()
    motorb1.low()
    motorb2.low()

def bncs():
    blancas.value(1)

def ver():
    verdes.value(1)

def bocina():
    buzzer.freq(500)
    buzzer.duty_u16(10000)

def rjas():
    rojas.value(1)
def detecta():
    parar()
    rjas()
    bocina()
    bncs()    
    utime.sleep(0.3)
    blancas.value(0)
    rojas.value(0)
    buzzer.duty_u16(0)

def inicio():
  
 
  def playNote(frequency, duration, pause) :
      global buzzer
      buzzer.duty_u16(10000)  # ajusta el volumen
      buzzer.freq(frequency)
      time.sleep(duration)
      buzzer.duty_u16(0) #apaga el buzzer
      time.sleep(pause)
   # notas que seran escuchadas en el buzzer  
  notes = [440, 494, 523, 587, 659, 698, 784]
  #secuencia for para tocar las notas 
  for note in notes :
      playNote(note, 0.1, 0.1 )
      blancas.value(1)
      time.sleep(0.02)
      blancas.value(0)
      time.sleep(0.02)
      verdes.value(1)
      time.sleep(0.02)
      verdes.value(0)
      time.sleep(0.02)
      rojas.value(1)
      time.sleep(0.02)
      rojas.value(0)
def ultrasonido():
    # Enviar pulso para activar el sensor de ultrasonido
    trig.low()
    utime.sleep_us(2)
    trig.high()
    utime.sleep_us(10)
    trig.low()

    # Medir el tiempo que tarda en recibir el eco
    while echo.value() == 0:
        pulse_start = utime.ticks_us()

    while echo.value() == 1:
        pulse_end = utime.ticks_us()

    pulse_duration = utime.ticks_diff(pulse_end, pulse_start)

    # Calcular la distancia en cm
    distancia = pulse_duration * 0.0343 / 2

    return distancia
#usa el segundo nucleo para la funcion inicio
_thread.start_new_thread(inicio,())
''' control bluetooth: resicibe los caracteres maracdos con ""
    y llama  a las diferentes funciones ''' 
while True:
    if modulo.any() > 0:
        dato = modulo.read(1)
        dato = dato.decode().strip()
        print(dato)
        if dato == "F":
            adelante()
        elif dato == "B":
            atras()
        elif dato == "R":
            izquierda()
        elif dato == "L":
            derecha()
        elif dato == "S":
            parar()   
        elif dato == "W":
            bncs()
        elif dato == "w":
            blancas.value(0)
        elif dato == "U":
            ver()
        elif dato == "u":
            verdes.value(0)
        elif dato == "X":
             inicio()
        elif dato == "V":
            bocina()
        elif dato == "v":
            buzzer.duty_u16(0)
    # Comprobar distancia con el sensor de ultrasonido
    distancia_actual = ultrasonido()
    '''si la distancia es menor a 15cm y recibe el caracter "F"
       llama a la funcion detecta'''
    if distancia_actual <15 and dato == "F":
            detecta()   
         
