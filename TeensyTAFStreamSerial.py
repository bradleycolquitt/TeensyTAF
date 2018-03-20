import sys
import os
import time
import datetime
import serial
from serial.tools import list_ports



date = datetime.datetime.now()
ser=serial.Serial("/dev/ttyACM0",115200)
outfile=open('./'+str(date[0])+','+str(date[1])+','+str(date[2])+','+str(date[3])+'test'+'.TAFlog','a')

looper=1;

while (looper==1):
         
         if (ser.inWaiting()>0):
             
           line=ser.readline(ser.inWaiting()) #.strip('\r'));
           outfile.write(line.strip('\r\n'))
           
           sys.stdout.write(line.strip('\r\n'));
           sys.stdout.flush();
           for c in line:
                if (c) == '\n':           
                   outfile.write(','time.time() +'\n');           
                   sys.stdout.write('\n');
                   sys.stdout.flush();

           
           
           
