import threading
import sys, os, signal
import subprocess
import time
from datetime import datetime


def findip(n, subnet='10.0.0.' ):
    for i in range(n*3, (n+1)*3):
        command_line = 'ping -a -n 1 ' + subnet + str(i)
        # command_line = 'ping -4 -a -n 1 ' + 'WGC100DFH0NQ2'
        # print(command_line)
        try:
            output = subprocess.check_output(command_line)
            name_ip = str(output).split('Pinging')[1].split('with')[0]
            print(name_ip)
        except Exception as e:
            print(' empty_ip .' + str(i))


if __name__ =="__main__":  
    subnet = input('subnet starts 10.0.0. ? : ')  
    start = datetime.now()   

    if subnet == '':
        subnet = '10.0.0.'
        scan_scope = 5
    else:
        scan_scope = int(input('scan scope 3x:'))
        
    for n in range(scan_scope):
        globals()[f'threading{n}'] = threading.Thread(target=findip, args=(n, subnet))
        globals()[f'threading{n}'].start()
        # print('open threading ...', n)
    time.sleep(3)
    for n in range(scan_scope):   
        globals()[f'threading{n}'].join()
        # print('close threading ...', n)

end = datetime.now()
print('scan time : ' + str(end - start).split('.')[0])






'''
pid = os.getpid()
print(f"ID of process: {pid}")
print("Main thread name: {}".format(threading.current_thread().name))

time.sleep(2)
os.kill(int(pid), signal.SIGTERM)
print(f"{pid} is terminated")    

sys.exit()
'''