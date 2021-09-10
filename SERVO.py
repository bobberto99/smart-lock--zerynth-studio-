# import the streams module, it is needed to send data around
import streams

# open the default serial port, the output will be visible in the serial console
streams.serial()  

import pwm
motore=None

class servo:
    #definisco il pin in cui é inserito il servomotore e lo inizializzo in modalitá PWM con posizione a 0 gradi
    def __init__(self,funpin=D10):
        #setup del pin
        global motore
        self.pin=funpin
        motore=D10.PWM
        pinMode(self.pin,OUTPUT)
        self.PERIOD=None
        self.PULSE=None
        #rotazione fino a posizione di 0 gradi
        self.ruota_al_centro()
    
        #definisco la funzione che permette la rotazione del servomotore a destra
    def ruota_a_destra(self):
        self.PULSE=2500
        pwm.write(motore,self.PERIOD,self.PULSE,MICROS)
        print("il servomotore ruota a destra")
        sleep(1000)
    
        #definisco la funzione che permette la rotazione del servomotore a sinistra
    def ruota_a_sinistra(self):
        self.PULSE=500
        pwm.write(motore,self.PERIOD,self.PULSE,MICROS)
        print("il servomotore ruota a sinistra")
        sleep(1000)
    
        #definisco la funzione che permette di resettare la posizione del servomotore
    def ruota_al_centro(self):
        self.PERIOD=20000
        self.PULSE=1500
        pwm.write(motore,self.PERIOD,self.PULSE,MICROS)
        print("il servomotore ruota in poszione centrale")
        sleep(1000)
    
        #definisco la funzione che permette di ruotare manualmente il servomotore
    def ruota_manualmente(self,PULSE=1500):
        self.PULSE=PULSE
        pwm.write(motore,self.PERIOD,self.PULSE,MICROS)
        print("il servomotore sta ruotando")
        sleep(1000)
    
        #definisco la funzione che permette di conoscere la posizione attuale del servomotore
    def posizione(self):
        if (self.PULSE==1500):
            print("il servomotore é in poszione centrale")
        if (self.PULSE>1500):
            print("il servomotore é ruotato verso destra")
        if (self.PULSE<1500):
            print("il servomotore é ruotato verso sinistra")