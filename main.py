# 
# Created at 2021-08-18 13:36:17.112371

import streams
import DEVICE
import FUNZIONI


#azioni pre inizializzazione
streams.serial()


#inizio del processo principale

print("progetto iniziato")

#inizializzazione device

device=DEVICE.device()




if device.fail==False:
    payload={"stato" : "accesso eseguito"}
    tag="stato"
    device.zdmdevice.publish(payload, tag)
    print("prima publish completata")
    stato=device.close_device(device=device.zdmdevice)
    print("dispositivo chiuso")
    device.led.stop_blinking()                                                  #il led smette di lampeggiare
    chr=""                                                  #variabile inizializzata per il check sotto
    thread(FUNZIONI.publish_thread,(device))
    sleep(1000)
    #fine inizializzazione dispositivo
    
    
    #inizio del ciclo infinito che controlla lo stato
    i=0
    while True:
        
        if (device.device_status()!="aperto" and device.device_status()!="manomesso"):
            if device.led.is_blinking()== True:
                device.led.stop_blinking()
            device.led.onblue()
            print("controllo richiesta inserimento password")
            chr=device.tastierino.leggi_elemento()
            if(chr=='D'):
                
                print("INIZIO LETTURA DELLA PASSWORD!")
                accesso_eseguito=device.login()
                print("controllo accesso eseguito")
                
                if(accesso_eseguito==True):
                    
                    print("avvio apertura dispositivo")
                    device.open_device(device=device.zdmdevice)
                    print("fine apertura dispositivo")
            device.check_manumission()
        
        
        
        #definisco il funzionamento del dispositivo in caso di manomissione, questa parte di funzione viene eseguita solo 1 volta per manomissione
        elif (device.device_status()=="manomesso" and device.led.is_blinking() == False):
            
            device.led.ledoff()
            sleep(500)
            device.led.onred()
            device.led.start_blinking(150)
        
        
        
        elif (device.device_status() == "aperto"):
            chr=""
            device.led.ongreen()
            print("controllo richiesta chiusura del dispositivo")
            chr=device.tastierino.leggi_elemento()
            if(chr=='D'):
                device.close_device()
        
        
        
        sleep(500)