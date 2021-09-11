import adc
import FUNZIONI


def control_thread(device):
    print("thread avviato!\n")
    while device.fotoresistore.fine==False:
        if(device.fotoresistore.valore_base < 10000 and device.device_status()=="chiuso"):
            valore=device.fotoresistore.lettura_luce()
            if valore<device.fotoresistore.valore_base:
                device.fotoresistore.allarme=True
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



    def start_thread(self,device):
        self.fine=False
        print("avvio thread lettura luce del fotoresistore\n")
        thread(control_thread, (device) )
        print("thread lettura luce del fotoresistore avviato correttamente!")



    def stop_thread(self):
        self.fine=True


    def stop_allarm(self):
        self.allarme=False



    def check_allarm(self):
        return self.allarme



    def set_valore_base(self, valore):
        print("aggiornamento valore base del resistore!")
        self.valore_base=valore
        print("nuovo valore= ",self.valore_base)