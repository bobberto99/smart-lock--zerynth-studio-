import RGB_LED
import SERVO
import KEYPAD
import FOTORESISTORE
import socket
from zdm import zdm
from espressif.esp32net import esp32wifi as wifi_driver
from wireless import wifi






class device:
    
    
    def __init__(self):
        self.stato=None
        self.password=None
        self.set_password("1234")   #funzione utilizzata per impostare la password iniziale PROBABILMENTE DA MODIFICARE
        
        
        connectionerr=False                #variabile utilizzata per vedere se la connessione é andata o meno a buon fine
        self.fail=False                      #variabile utilizzata per il controllo della connessione alla zdm
        
        
        wifi_id="Vodafone2.5"           #variabile utilizzata per inserire l'ID del wifi
        wifi_pass="applekskkdbmu37k"    #variabile utilizzata per inserire la password del wifi
        
        
        print("inizializzazione device!")
        self.led= RGB_LED.led()
        print("led inizializzato")
        self.led.onblue()
        self.led.start_thread()
        self.led.start_blinking(200)
        sleep(1000)
        
        
        self.servo=SERVO.servo()
        print("servo inizializzato")
        sleep(1000)
        
        
        self.tastierino=KEYPAD.Keypad()
        print("tastierino inizializzato")
        sleep(1000)
        
        
        self.fotoresistore=FOTORESISTORE.fotoresistore()
        self.fotoresistore.start_thread(self)
        print("fotoresistore inizializzato")
        
        
        print("componenti inizializzati")
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
            connectionerr=True
            self.fail=True
        
        
        #inizializzo lo zdm
        if connectionerr==False:
            try:
                print("inizializzazione zdm")
                
                #definisco il dizionario dei jobs
                
                my_jobs = {
                    'finemanomissione' : self.end_manumission_job,
                    'setpassword' : self.set_password,
                    'apridispositivo' : self.open_device,
                    'chiudidispositivo' : self.close_device,
                    'statodispositivojob' : self.device_status_job,
                    }
                
                
                self.zdmdevice=zdm.Device(condition_tags=["stato"],jobs_dict=my_jobs)
                print("fine inizializzazione zdm")
                
                
                print("connessione zdm")
                self.zdmdevice.connect()
                print("connessione effettuata")
                
                
                #creo 3 condizioni per lo zdm
                
                
                print("inizio definizione condizioni zdm.")
                self.manomissionecond=self.zdmdevice.new_condition("stato")
                self.chiusocond=self.zdmdevice.new_condition("stato")
                self.apertocond=self.zdmdevice.new_condition("stato")
                print("fine definizione condizioni zdm.")
                
                
                
                
            except Exception as e:
                print("errore: ",e)
                self.fail=True



    def login(self):
        i=0
        x=0
        accesso=False
        password=""
        while accesso == False and x<3:
            while i<4:
                
                if (self.fotoresistore.check_allarm() == False):
                    print ("inizio controllo!")
                    self.led.onblue()
                    self.led.start_blinking(150)
                    sleep(2000)
                    elemento=self.tastierino.leggi_elemento()
                    self.led.stop_blinking()
                    
                    if (elemento != "error"):
                        i+=1
                        password+=elemento
                        print(password)
                        sleep(1000)
                    else:
                        self.led.ledoff()
                        sleep(1000)
                        print("password non aggiornata!")
                        print("numero di elementi inseriti nella password= ",i)
                        self.led.onred()
                        self.led.blink(200,4)
                        self.led.ledoff()
                        
                else:
                    print("manomissione durante la lettura!")
                    return False
            
            print("controllo password.")
            print("password inserita= ",password)
            if(self.password==password):
                accesso=True
            else:
                self.led.ledoff()
                accessp=False
                x+=1
                self.led.onred()
                self.led.blink(100,8)
                i=0
                password=""
        if (accesso== False):
            print("accesso negato!")
            sleep(1000)
            payload={"accesso" : "accesso negato"}
            tag="accesso"
            self.zdmdevice.publish(payload,tag)
        return accesso



    def close_device(self,device=None,arg=None):
        self.servo.ruota_al_centro()
        valore=self.fotoresistore.lettura_luce()-600
        print("valore del fotoresistore: ",valore)
        self.fotoresistore.set_valore_base(valore)
        self.stato="chiuso"
        print("dispositivo chiuso.")
        self.zdmdevice.publish({"stato" : self.stato} ,"stato")
        if not self.chiusocond.is_open():
            print("chiusura condizioni precedenti!")
            if self.manomissionecond.is_open():
                self.manomissionecond.close(payload={"stato" : "stato dispositivo passato a chiuso"})
                sleep(400)
            if self.apertocond.is_open(): 
                self.apertocond.close(payload={"stato" : "stato dispositivo passato a chiuso"})
                sleep(400)
            print("reset condizione chiusura.")
            self.chiusocond.reset()
            print("apertura nuova condizione chiusura.")
            self.chiusocond.open(payload={"stato" : "dispositivo chiuso"})
        return self.stato



    def open_device(self,device=None,arg=None):
        self.servo.ruota_a_sinistra()
        self.stato="aperto"
        print("dispositivo aperto.")
        self.zdmdevice.publish({"stato" : self.stato} ,"stato")
        if not self.apertocond.is_open():
            print("chiusura condizioni precedenti!")
            if self.manomissionecond.is_open():
                self.manomissionecond.close(payload={"stato" : "stato dispositivo passato ad aperto"})
                sleep(400)
            if self.chiusocond.is_open():
                self.chiusocond.close(payload={"stato" : "stato dispositivo passato ad aperto"})
                sleep(400)
        print("reset condizione apertura.")
        self.apertocond.reset()
        print("avvio nuova condizione apertura.")
        self.apertocond.open(payload={"stato" : "dispositivo aperto"})
        return self.stato



    def manumission_device(self,device=None,arg=None):
        self.servo.ruota_al_centro()
        self.stato="manomesso"
        print("dispositivo manomesso.")
        self.zdmdevice.publish({"stato" : self.stato} ,"stato")
        if not  self.manomissionecond.is_open():
            print("chiusura condizioni precedenti!")
            if self.chiusocond.is_open():
                self.chiusocond.close(payload={"stato" : "stato dispositivo manomesso!"})
            if self.apertocond.is_open():
                self.apertocond.close(payload={"stato" :"stato dispositivo manomesso!"})
            print("reset condizione di manomissione.")
            self.manomissionecond.reset()
            print("apertura nuova condizione di manomissione.")
            self.manomissionecond.open(payload={"stato" : "dispositivo manomesso"})
        return self.stato



    def end_manumission_job(self,device=None,arg=None):
        print("avvio fine manomissione.")
        self.close_device()
        self.fotoresistore.stop_allarm()
        print("stato di allarme del fotoresistore= ",self.fotoresistore.allarm)
        print("Fine manomissione")



    def device_status(self):
        return self.stato



    def device_status_job(self,device=None,arg=None):
        self.zdmdevice.publish({"stato" : self.stato}, "stato")



    def set_password(self,device=None,arg="1234"):
        self.password=arg
        print("password aggiornata!")
        print(arg,"      ",self.password)



    #definisco la funzione che viene utilizzata per controllare se il dispositivo viene manomesso
    def check_manumission (self):
        print("avvio controllo manomissione.")
        allarm=self.fotoresistore.check_allarm()
        print("valore allarme: ", allarm)
        if allarm == True:
            self.manumission_device()
        print("fine controllo allarme.")

