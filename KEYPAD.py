# test keypad
# Created at 2021-08-03 13:25:33.922390
import streams

streams.serial()
#definisco i pin a livello globale
PIN8=None
PIN7=None
PIN6=None
PIN5=None
PIN4=None
PIN3=None
PIN2=None
PIN1=None
#imposto il tempo di stabilizzazione del segnale
debouncetime=20


class Keypad:
    #INIZIALIZZAZIONE DEL DISPOSITIVO, SUPPORTA SOLO KEYPAD A 4 RIGHE E COLONNE
    def __init__(self, PIN08, PIN07, PIN06, PIN05, PIN04, PIN03, PIN02, PIN01):
        #Inizializzo le variabili globali che si riferiscono ai pin
        global PIN8,PIN7,PIN6,PIN5,PIN4,PIN3,PIN2,PIN1
        PIN8=PIN08
        PIN7=PIN07
        PIN6=PIN06
        PIN5=PIN05
        PIN4=PIN04
        PIN3=PIN03
        PIN2=PIN02
        PIN1=PIN01
        #salvo le tuple delle righe e delle colonne nella classe
        self.righe=(PIN8,PIN7,PIN6,PIN5)
        self.colonne=(PIN4,PIN3,PIN2,PIN1)
        for x in self.righe:
            pinMode(x,INPUT_PULLUP)
            print("riga:",x," inizializzata" )
            digitalWrite(x,HIGH)
            sleep(100)
        for x in self.colonne:
            pinMode(x,OUTPUT)
            print("colonna", x," inizializzata")
            digitalWrite(x,HIGH)
            sleep(100)


    def leggi_elemento(self):
        print("avvio lettura della tastiera \n")
        pinpremuti="nessun elemento"
        char=""
        #attivo la colonna corrente per la lettura
        for x in self.colonne:
            digitalWrite(x,LOW)
            for y in self.righe:
                if (digitalRead(y)==LOW):
                    sleep(debouncetime)
                    pinpremuti=(x,y)
            sleep(500)
            digitalWrite(x,HIGH)
        if(type(pinpremuti)==type("stringa")):
            return "error"
        if(PIN8==pinpremuti[1] and PIN4==pinpremuti[0]):
            char="1"
        if(PIN8==pinpremuti[1] and PIN3==pinpremuti[0]):
            char="2"
        if(PIN8==pinpremuti[1] and PIN2==pinpremuti[0]):
            char="3"
        if(PIN8==pinpremuti[1] and PIN1==pinpremuti[0]):
            char="a"
        if(PIN7==pinpremuti[1] and PIN4==pinpremuti[0]):
            char="4"
        if(PIN7==pinpremuti[1] and PIN3==pinpremuti[0]):
            char="5"
        if(PIN7==pinpremuti[1] and PIN2==pinpremuti[0]):
            char="6"
        if(PIN7==pinpremuti[1] and PIN1==pinpremuti[0]):
            char="B"
        if(PIN6==pinpremuti[1] and PIN4==pinpremuti[0]):
            char="7"
        if(PIN6==pinpremuti[1] and PIN3==pinpremuti[0]):
            char="8"
        if(PIN6==pinpremuti[1] and PIN2==pinpremuti[0]):
            char="9"
        if(PIN6==pinpremuti[1] and PIN1==pinpremuti[0]):
            chqr="c"
        if(PIN5==pinpremuti[1] and PIN4==pinpremuti[0]):
            char="*"
        if(PIN5==pinpremuti[1] and PIN3==pinpremuti[0]):
            char="0"
        if(PIN5==pinpremuti[1] and PIN2==pinpremuti[0]):
            char="#"
        if(PIN5==pinpremuti[1] and PIN1==pinpremuti[0]):
            char="D"

        return char