from serial.tools import list_ports
import subprocess as sp
from threading import Thread


threads = []
for com in list(list_ports.comports()):
    print(":", com.device, ":")

    th = Thread(target=sp.run, args=(f"python flash_once.py {com}",))
    th.start()
    threads.append(th)

for thread in threads:
    thread.join()
