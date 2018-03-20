#! /usr/bin/env python


import time
import lib.audiorecording_tools as at

import sys
import os
import re
import time
import datetime
import serial
import multiprocessing as mp
from serial.tools import list_ports



# date = datetime.datetime.now()
# ser=
# bird = 'test_teensy'

# outfile_fn = 
# outfile=open(outfile_fn,'a')


class TeensyTAF:
    def __init__(self):
        self.inital_date = datetime.datetime.now()
        self.serial_con = serial.Serial("/dev/ttyACM0",115200)
        self.audio_recorder = at.AudioRecord()

    def init_config(self, config_file):
        self.audio_recorder.init_config(config_file)
        self.outdir = self.audio_recorder.params['outdir']
        self.outdir_serial = '/'.join([self.outdir, 'TAFlogs'])

        if not os.path.exists(self.outdir_serial):
            os.makedirs(self.outdir_serial)
        self.serial_fn = '/'.join([self.outdir_serial,  self.inital_date.strftime("%y%m%d") + '.TAFlog'])
        print(self.serial_fn)
        self.serial_fp = open(self.serial_fn, 'a')
        
    def start_serial_recorder(self):
        self.serial_recorder = mp.Process(target = serial_recorder_loop, args = (self.serial_con,
                                                                                 self.serial_fp))
        self.serial_recorder.start()
    
       
def serial_recorder_loop(serial_con, serial_fp):
    line_out = ''
    while True:
        if (serial_con.inWaiting()>0):
            line=serial_con.readline(serial_con.inWaiting()) #.strip('\r'));
            line_out = ''.join([line_out, line.strip('\r\n')])
            if re.search('\n', line):
                line_out = ','.join([str(time.time()), line_out])
                serial_fp.write(line_out + '\n');
                serial_fp.flush()
                print(line_out)
                line_out = ''

if __name__=='__main__':
    ## Settings (temporary as these will be queried from GUI)
    import sys
    if len(sys.argv) <= 1:
        raise(Exception('No configuration file passed'))
    else:
        cfpath = sys.argv[1]

    tt = TeensyTAF()
    tt.init_config(cfpath)
    tt.audio_recorder.start()
    tt.start_serial_recorder()
