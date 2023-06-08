import threading
import sys, os, signal
import subprocess
import time
from datetime import datetime

start = datetime.now()


def findip(n):
    for i in range(n*3, (n+1)*3):
        command_line = 'ping -a -n 1 ' + '10.0.0.' + str(i)
        # command_line = 'ping -4 -a -n 1 ' + 'WGC100DFH0NQ2'
        # print(command_line)
        try:
            output = subprocess.check_output(command_line)
            name_ip = str(output).split('Pinging')[1].split('with')[0]
            print(name_ip)
        except Exception as e:
            print(' empty_ip .' + str(i))


if __name__ =="__main__":
    
    for n in range(5):
        globals()[f'threading{n}'] = threading.Thread(target=findip, args=(n,))
        globals()[f'threading{n}'].start()
        # print('open threading ...', n)
    time.sleep(3)
    for n in range(5):   
        globals()[f'threading{n}'].join()
        # print('close threading ...', n)

end = datetime.now()
print(str(end - start).split('.')[0])






'''
pid = os.getpid()
print(f"ID of process: {pid}")
print("Main thread name: {}".format(threading.current_thread().name))

time.sleep(2)
os.kill(int(pid), signal.SIGTERM)
print(f"{pid} is terminated")    

sys.exit()
'''