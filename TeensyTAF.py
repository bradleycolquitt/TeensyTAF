#! /usr/bin/env python


import time
import lib.audiorecording_tools as at
import ConfigParser
import sys
import os
import re
import time
import datetime
import serial
import multiprocessing as mp
import lib.GS_timing as gs
from serial.tools import list_ports



# date = datetime.datetime.now()
# ser=
# bird = 'test_teensy'

# outfile_fn = 
# outfile=open(outfile_fn,'a')


        
class TeensyTAF:
    def __init__(self):
        self.inital_date = datetime.datetime.now()
        dev_path = "/dev"
        possible_cons = ['/'.join([dev_path, a]) for a in os.listdir(dev_path) if re.search("ACM", a)]
        print(possible_cons)
        self.serial_con = serial.Serial(possible_cons[0],115200)
        self.audio_recorder = at.AudioRecord()

    def init_config(self, config_file):
        self.audio_recorder.init_config(config_file)
        self.outdir = self.audio_recorder.params['outdir']
        self.outdir_serial = '/'.join([self.outdir, 'TAFlogs'])
        if not os.path.exists(self.outdir_serial):
            os.makedirs(self.outdir_serial)

        self.outdir_config = '/'.join([self.outdir, 'configs'])
        if not os.path.exists(self.outdir_config):
            os.makedirs(self.outdir_config)

        self.serial_fn = '/'.join([self.outdir_serial,  self.inital_date.strftime("%y%m%d_%H%M%S") + '.TAFlog'])
        print(self.serial_fn)
        self.serial_fp = open(self.serial_fn, 'a')
        self.teensy_config_file = None
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        section = 'teensy_params'
        if config.has_section(section):
            option = 'teensy_variables'
            if config.has_option(section, option):
                self.teensy_config_file = config.get(section,option)

    def start_serial_recorder(self):
        self.serial_recorder = mp.Process(target = serial_recorder_loop, args = (self.serial_con,
                                                                                 self.serial_fp))
        self.serial_recorder.start()

    def read_teensy_config(self):
        if not self.teensy_config_file is None:
            config_file = open(self.teensy_config_file)
            for line in config_file:
                if re.search('//', line):
                    continue
                line = line.replace("#define ", "")
                line = line.replace(" ", ",")
                print(line)
                self.serial_fp.write(line)
            self.serial_fp.flush()

        # Copy teensy config to data_dir
        config_out_fname = '/'.join([self.outdir_config, "-".join(['config_variables', self.inital_date.strftime("%y%m%d_%H%M%S")]) + '.h'])
        shutil.copy(self.teensy_config_file,)

def serial_recorder_loop(serial_con, serial_fp):
    line_out = ''
    event_num = 1
    while True:
        if (serial_con.inWaiting()>0):
            line=serial_con.readline(serial_con.inWaiting()) #.strip('\r'));
            line_out = ','.join([line_out, line.strip('\r\n')])

            #if re.search('PSD', line):
                
            if re.search('\n', line):
                line_out = ','.join([str(time.time())
                                    , str(event_num), line_out])
                # line_out = ','.join([str(gs.millis()/1000),
                #                          str(event_num), line_out])
                line_out = re.sub(',,',',', line_out)
                serial_fp.write(line_out + '\n');
                serial_fp.flush()
                print(line_out)
                event_num += 1
                line_out = ''

def serial_recorder_loop_json(serial_con, serial_fp):
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
    tt.read_teensy_config()
    tt.start_serial_recorder()
