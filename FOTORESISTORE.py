import adc
import streams
import FUNZIONI

def control_thread(fotoresistore):
    print("thread avviato!\n")
    while fotoresistore.fine==False:
        if(fotoresistore.valore_base < 10000 and FUNZIONI.stato_dispositivo()=="chiuso"):
            fotoresistore.valore=fotoresistore.lettura_luce()
            if fotoresistore.valore<fotoresistore.valore_base:
                fotoresistore.allarme=True
        sleep(1000)
    print("fine thread lettura luce del fotoresistore\n")



class fotoresistore:
    def __init__(self,pin=A0):
        self.pin=pin
        pinMode(self.pin,INPUT_ANALOG)
        self.valore=None
        self.fine=None
        self.valore_base=10000
        self.allarme=False



    def lettura_luce(self):
        return adc.read(self.pin)



    def start_thread(self):
        self.fine=False
        print("avvio thread lettura luce del fotoresistore\n")
        thread(control_thread, (self) )
        print("thread lettura luce del fotoresistore avviato correttamente!")



    def stop_thread(self):
        self.fine=True


    def stop_allarm(self):
        self.allarm=False



    def check_allarm(self):
        return self.allarme



    def set_valore_base(self, valore):
        print("aggiornamento valore base del resistore!")
        self.valore_base=valore
        print("nuovo valore= ",self.valore_base)