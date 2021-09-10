# 
# Created at 2021-08-18 13:36:17.112371

import streams
import RGB_LED
import SERVO
import KEYPAD
import FOTORESISTORE
import FUNZIONI
import socket
import streams
from zdm import zdm
from espressif.esp32net import esp32wifi as wifi_driver
from wireless import wifi

#azioni pre inizializzazione
streams.serial()
connection=False                #variabile utilizzata per vedere se la connessione é andata o meno a buon fine
fail=False                      #variabile utilizzata per il controllo della connessione alla zdm
fine=0                          #variabile usata per controllare il blink_thread
FUNZIONI.set_password("1234")
wifi_id="Vodafone2.5"           #variabile utilizzata per inserire l'ID del wifi
wifi_pass="applekskkdbmu37k"    #variabile utilizzata per inserire la password del wifi












#definisco il dizionario dei jobs
my_jobs = {
    'finemanomissione' : FUNZIONI.fine_manomissione_job,
    'setpassword' : FUNZIONI.set_password,
    'apridispositivo' : FUNZIONI.apri_dispositivo,
    'chiudidispositivo' : FUNZIONI.chiudi_dispositivo,
    'statodispositivojob' : FUNZIONI.stato_dispositivo_job,
}



#inizio del processo principale



print("progetto iniziato")

#inizio inizializzazione dispositivo

# inizializzo i vari componenti

print("inizializzazione componenti")
led= RGB_LED.led()
print("led inizializzato")
led.onblue()
led.start_thread()
led.start_blinking(200)
sleep(1000)
servo=SERVO.servo()
print("servo inizializzato")
sleep(1000)
tastierino=KEYPAD.Keypad(D9,D13,D15,D2,D16,D4,D5,D22)
print("tastierino inizializzato")
sleep(1000)
fotoresistore=FOTORESISTORE.fotoresistore()
fotoresistore.start_thread()
print("fotoresistore inizializzato")
sleep(1000)
print("componenti inizializzati")
sleep(2000)
FUNZIONI.set_componenti(servo,fotoresistore)

#inizializzo il wifi

print("inizializzo il driver del wifi")
sleep(1000)
wifi_driver.auto_init()
print("driver wifi inizializzato")
sleep(1000)

try:
    print("provo a connettermi al wifi")
    wifi.link(wifi_id,wifi.WIFI_WPA2,wifi_pass)
    print("connessione eseguita")
    sleep(3000)

except Exception as e:
    print("eccezione: ",e)
    connection=True


#inizializzo lo zdm
if connection==False:
    try:
        print("inizializzazione zdm")
        zdmdevice=zdm.Device(condition_tags=["stato"],jobs_dict=my_jobs)
        print("fine inizializzazione zdm")
        print("connessione zdm")
        zdmdevice.connect()
        print("connessione effettuata")
    except Exception as e:
        print("errore: ",e)
        fail=True


    #creo 3 condizioni per lo zdm
    print("inizio definizione condizioni zdm")
    manomissionecond=zdmdevice.new_condition("stato")
    chiusocond=zdmdevice.new_condition("stato")
    apertocond=zdmdevice.new_condition("stato")
    print("fine definizione condizioni zdm")
    print("inizio spostamento variabili in FUNZIONI")
    FUNZIONI.set_zdmdevice(zdmdevice,manomissionecond,chiusocond,apertocond)
    print("fine spostamento variabili in FUNZIONI")




if fail==False:
    print("fail == false")
    payload={"stato" : "accesso eseguito"}
    tag="stato"
    zdmdevice.publish(payload, tag)
    print("prima publish completata")
    stato=FUNZIONI.chiudi_dispositivo(device=zdmdevice)
    print("dispositivo chiuso")
    led.stop_blinking()                                                  #il led smette di lampeggiare
    chr=""                                                  #variabile inizializzata per il check sotto
    thread(FUNZIONI.publish_thread,(zdmdevice))
    sleep(1000)
    #fine inizializzazione dispositivo
    
    
    #inizio del ciclo infinito che controlla lo stato
    i=0
    while True:
        
        if (FUNZIONI.stato_dispositivo()!="aperto" and FUNZIONI.stato_dispositivo()!="manomesso"):
            if led.is_blinking()== True:
                led.stop_blinking()
            led.onblue()
            print("controllo richiesta inserimento password")
            chr=tastierino.leggi_elemento()
            if(chr=='D'):
                
                print("INIZIO LETTURA DELLA PASSWORD!")
                accesso_eseguito=FUNZIONI.esegui_accesso(led,tastierino,fotoresistore)            #da migliorare il controllo utilizzare if prima del controllo inserimento tasto ( all'interno di funzioni) cosí da poter controllare la manomissione
                print("controllo accesso eseguito")
                
                if(accesso_eseguito==True):
                    
                    print("avvio apertura dispositivo")
                    FUNZIONI.apri_dispositivo(device=zdmdevice)
                    print("fine apertura dispositivo")
                    
                elif(accesso_eseguito==False):
                    
                    print("avvio segnalazione errore")
                    FUNZIONI.errore_accesso(zdmdevice)
                    print("fine segnalazione errore")
                    led.onblue()
            FUNZIONI.controllo_manomissione(fotoresistore)
        
        
        
        #definisco il funzionamento del dispositivo in caso di manomissione, questa parte di funzione viene eseguita solo 1 volta per manomissione
        elif (FUNZIONI.stato_dispositivo()=="manomesso" and led.is_blinking() == False):
            
            led.ledoff()
            sleep(500)
            led.onred()
            led.start_blinking(150)
        
        
        
        elif (FUNZIONI.stato_dispositivo()=="aperto"):
            chr=""
            led.ongreen()
            print("controllo richiesta chiusura del dispositivo")
            chr=tastierino.leggi_elemento()
            if(chr=='D'):
                FUNZIONI.chiudi_dispositivo()
        
        
        
        sleep(500)