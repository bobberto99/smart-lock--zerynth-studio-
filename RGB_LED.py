import streams
import threading

#avvio lo stream sulla porta seriale
streams.serial()
lock=threading.Lock()
#funzione utilizzata per creare un thread che permette alla led di lampeggiare
def blink_thread(led):
    print("thread avviato!\n")
    while led.fine==False:
        if led.lampeggia==True:
            print("il led inizia a lampeggiare \n")
            while led.lampeggia==True:
                lock.acquire()
                led.blink(led.time,1)
                lock.release()
            print("il led smette di lampeggiare \n")
        else:
            sleep(1000)




class led:
    def __init__(self,RED=D14,GREEN=D27,BLUE=A1):
        print("inizializzazione rgb led")
        #SALVO LE VARIABILI DEI PIN NELL'OGGETTO
        self.RED=RED
        self.GREEN=GREEN
        self.BLUE=BLUE
        #INIZIALIZZO LE VARIABILI
        pinMode(self.RED,OUTPUT)
        pinMode(self.BLUE,OUTPUT)
        pinMode(self.GREEN,OUTPUT)
        #SPENGO IL LED DI STANDARD
        digitalWrite(self.RED,LOW)
        digitalWrite(self.BLUE,LOW)
        digitalWrite(self.GREEN,LOW)
        self.ledstatus="led spento"
        print("inizializzazione rgb led terminata, pin inizializzati: \n ROSSO= ",RED,"\n BLUE= ",BLUE,"\n VERDE= ", GREEN)
        #definisco le variabili da utilizzare in caso di threads
        self.fine=False
        self.lampeggia=False
        self.time=0
    
    def onblue (self):
        digitalWrite(self.BLUE,HIGH)
        digitalWrite(self.GREEN,LOW)
        digitalWrite(self.RED,LOW)
        self.ledstatus="blue"



    def onred(self):
        digitalWrite(self.RED,HIGH)
        digitalWrite(self.BLUE,LOW)
        digitalWrite(self.GREEN,LOW)
        self.ledstatus="rosso"



    def ongreen(self):
        digitalWrite(self.GREEN,HIGH)
        digitalWrite(self.BLUE,LOW)
        digitalWrite(self.RED,LOW)
        self.ledstatus="verde"



    def ledoff(self):
        digitalWrite(self.RED,LOW)
        digitalWrite(self.BLUE,LOW)
        digitalWrite(self.GREEN,LOW)
        self.ledstatus="led spento"



    def blink(self,TIME,n):
        i=0
        if(self.ledstatus == "rosso"):
            while i<n:
                self.ledoff()
                sleep(TIME)
                self.onred()
                sleep(TIME)
                i+=1
        if(self.ledstatus == "verde"):
            while i<n:
                self.ledoff()
                sleep(TIME)
                self.ongreen()
                sleep(TIME)
                i+=1
        if(self.ledstatus == "blue"):
            while i<n:
                self.ledoff()
                sleep(TIME)
                self.onblue()
                sleep(TIME)
                i+=1
        if(self.ledstatus == "led spento"):
            print("led spento impossibile lampeggiare!")
            sleep(500)



    #funzione che avvia il thread
    def start_thread(self):
        self.fine=False
        self.lampeggia=False
        print("avvio thread che regola il lampeggio del led! \n")
        thread(blink_thread, (self) )
        print("thread che regola il lampeggio del led avviato correttamente")



    #la funzione permette al led di lampeggiare attraverso il thread
    def start_blinking(self,time):
        self.lampeggia=True
        self.time=time


    #la funzione permette al led di smettere di lampeggiare attraverso il thread
    def stop_blinking(self):
        lock.acquire()
        print("fine lampeggio!")
        self.lampeggia=False
        lock.release()



    #la funzione permette la fine del thread
    def end_thread(self):
        self.fine=True



    #la funzione permette di sapere se il thread sta lampeggiando
    def is_blinking(self):
        return self.lampeggia