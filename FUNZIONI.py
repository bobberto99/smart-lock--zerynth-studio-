import streams

streams.serial()



#aggiorno lo stato allo zdm ogni 10 minuti
def publish_thread(device):
    while True:
        stato=device.device_status()
        payload={ "stato" : device.stato  }
        device.zdmdevice.publish(payload , "stato")
        print("\nzdm aggiornata!\n")
        sleep(600000)