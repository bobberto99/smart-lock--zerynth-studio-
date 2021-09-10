codice="1234"
stato=""
servo=None
zdmdevice=None
manomissionecond=None
chiusocond=None
apertocond=None
fotoresistore=None


#funzione utilizzata per portare l'oggetto servomotore dal main al file
def set_componenti(servomain,fotoresistoremain):
    global servo
    global fotoresistore
    servo=servomain
    fotoresistore=fotoresistoremain



#funzione utilizzata per portare tutti i parametri della zdm nelle varie funzioni nel file
def set_zdmdevice(zdmdevicemain,manomissione,chiuso,aperto):
    global zdmdevice
    global manomissionecond
    global chiusocond
    global apertocond
    zdmdevice=zdmdevicemain
    manomissionecond=manomissione
    chiusocond=chiuso
    apertocond=aperto



#funzione che controlla la correttezza della password
def check_password(password):
    global codice
    print("password inserita: ",password)
    print("codice: ",codice)
    return password == codice



#funzione che chiude il dispositivo
def chiudi_dispositivo(device=zdmdevice, arg= None):
    global stato
    global servo
    global manomissionecond
    global chiusocond
    global apertocond
    global fotoresistore
    servo.ruota_al_centro()
    valore=fotoresistore.lettura_luce()-600
    print("valore del fotoresistore: ",valore)
    fotoresistore.set_valore_base(valore)
    stato="chiuso"
    print("dispositivo chiuso")
    zdmdevice.publish({"stato" : stato} ,"stato")
    if not chiusocond.is_open():
        if manomissionecond.is_open():
            manomissionecond.close(payload={"stato" : "stato dispositivo passato a chiuso"})
            sleep(400)
        if apertocond.is_open():
            apertocond.close(payload={"stato" : "stato dispositivo passato a chiuso"})
            sleep(400)
        print("reset condizione chiusura")
        chiusocond.reset()
        print("apertura nuova condizione chiusura")
        chiusocond.open(payload={"stato" : "dispositivo chiuso"})
    return stato



#funzione che apre il dispositivo
def apri_dispositivo(device=zdmdevice , arg= None):
    global stato
    global zdmdevice
    global servo
    global manomissionecond
    global chiusocond
    global apertocond
    sleep(500)
    servo.ruota_a_sinistra()
    stato="aperto"
    print("dispositivo aperto")
    zdmdevice.publish({"stato" : stato} ,"stato")
    if not apertocond.is_open():
        if manomissionecond.is_open():
            manomissionecond.close(payload={"stato" : "stato dispositivo passato ad aperto"})
            sleep(400)
        if chiusocond.is_open():
            chiusocond.close(payload={"stato" : "stato dispositivo passato ad aperto"})
            sleep(400)
        print("reset condizione apertura")
        apertocond.reset()
        print("avvio nuova condizione apertura")
        apertocond.open(payload={"stato" : "dispositivo aperto"})
    return stato



#funzione che segnala la manomissione del dispositivo
def errore_dispositivo(device=zdmdevice, arg= None):
    global stato
    global zdmdevice
    global servo
    global manomissionecond
    global chiusocond
    global apertocond
    servo.ruota_al_centro()
    stato="manomesso"
    print("dispositivo manomesso")
    zdmdevice.publish({"stato" : stato} ,"stato")
    if not manomissionecond.is_open():
        if chiusocond.is_open():
            chiusocond.close(payload={"stato" : "stato dispositivo manomesso!"})
        if apertocond.is_open():
            apertocond.close(payload={"stato" :"stato dispositivo manomesso!"})
        print("reset condizione di manomissione")
        manomissionecond.reset()
        print("apertura nuova condizione di manomissione")
        manomissionecond.open(payload={"stato" : "dispositivo manomesso"})
    return stato


#funzione che definisce la fine della manomissione
def fine_manomissione_job (device, arg= None):
    global fotoresistore
    print("avvio fine manomissione")
    chiudi_dispositivo()
    print("fine manomissione")
    fotoresistore.stop_allarm()



#funzione che controlla se il dispositivo é aperto, chiuso o in allarme
def stato_dispositivo():
    global stato
    return stato



#job che richiede manualmente lo stato del dispositivo
def stato_dispositivo_job(device=zdmdevice, arg= None):
    global zdmdevice
    global stato
    zdmdevice.publish({"stato" : stato},"stato")



#funzione che norifica l'errore sull'accesso allo zdm
def errore_accesso(zdmdevice):
    print("accesso negato")
    sleep(1000)
    payload={"accesso" : "accesso negato"}
    tag="accesso"
    zdmdevice.publish(payload, tag)



#funzione per cambiare la password, da attivare via la zdm
def set_password(device= zdmdevice, arg="1234"):
    global codice
    codice=arg
    print("password aggiornata!")
    print(arg,"        ", codice)
    return codice



#funzione che esegue tutti i passaggi per tentare di sbloccare il dispositivo La funzione ripete (per un max si 2 volte) la lettura della password dal tastierino, se la password inserita é quella giusta, esce dal while
#in caso di password errata ridá la possibilitá di reinserire la password!
def esegui_accesso(led,tastierino,fotoresistore):
    i=0
    password=""
    accesso_eseguito=False
    x=0
    while accesso_eseguito == False and x<3:
        #acquisisco la password dal tastierino
        while i<4:
            if(fotoresistore.check_allarm()==False):
                print("inizio controllo")
                led.onblue()                    #accendo il led fisso a blue
                led.start_blinking(150)
                sleep(1000)
                elemento=tastierino.leggi_elemento()
                led.stop_blinking()
                if(elemento != "error"):
                    i+=1
                    password+=elemento
                    print(password)
                    sleep(1000)
                else:
                    led.ledoff()
                    sleep(1000)
                    print("password non aggiornata!")
                    print("numero di elementi inseriti nella password= ",i)
                    led.onred()
                    led.blink(300,2)
                    led.ledoff()
            else:
                print("manomissione durante la lettura!")
                return False
        print("controllo password: ",password)
        accesso_eseguito=check_password(password)
        led.ledoff()
        if(accesso_eseguito==False):
            x+=1
            led.onred()
            led.blink(100,8)
            i=0
            password=""
    return accesso_eseguito



#definisco la funzione che viene utilizzata per controllare se il dispositivo viene manomesso
def controllo_manomissione (fotoresistore):
    print("avvio controllo manomissione.")
    allarm=fotoresistore.check_allarm()
    print("valore allarme: ", allarm)
    if allarm == True:
        errore_dispositivo()
    print("fine controllo allarme.")



#aggiorno lo stato allo zdm ogni 10 minuti
def publish_thread(zdmdevice):
    while True:
        stato=stato_dispositivo()
        payload={ "stato" : stato  }
        zdmdevice.publish(payload , "stato")
        print("\nzdm aggiornata!\n")
        sleep(600000)