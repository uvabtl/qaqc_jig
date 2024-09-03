import os
import sys
from datetime import datetime
from subprocess import Popen, PIPE
import subprocess

BAC = "UVA"


def read_box_temp():
    now = datetime.now()
    
    if BAC == "CERN":
        return []
    
    if BAC == "Milano":
        out = Popen(['tail','-n','1','/home/cmsdaq/DAQ/DHT22Logger/DHTLoggerData.log'],stdout=subprocess.PIPE)
        result = (out.stdout.read().decode().rstrip()).split()
        data_time = datetime.strptime(result[0]+" "+result[1].split('.')[0],"%Y-%m-%d %H:%M:%S")
        
        if abs(data_time-now).total_seconds() > 60.:
            raise ValueError("Could not read box temperature")
        else:
            return [float(result[2]),float(result[4]),float(result[6]),float(result[8]),float(result[10])]

    if BAC == "UVA":
        out = Popen(['tail','-n','1','/home/qaqcbtl/qaqc_jig/module_temps.log'],stdout=subprocess.PIPE)
        result = (out.stdout.read().decode().rstrip()).split()
        data_time = datetime.strptime(result[0]+" "+result[1].split('.')[0],"%Y-%m-%d %H:%M:%S")

        if abs(data_time-now).total_seconds() > 600.:
            raise ValueError("Could not read box temperature")
        else:
            return [float(r) for r in result[2:]]

def read_box_temp_hum():
    now = datetime.now()
    
    if BAC == "CERN":
        return []
    
    if BAC == "Milano":
        out = Popen(['tail','-n','1','/home/cmsdaq/DAQ/DHT22Logger/DHTLoggerData.log'],stdout=subprocess.PIPE)
        result = (out.stdout.read().decode().rstrip()).split()
        data_time = datetime.strptime(result[0]+" "+result[1].split('.')[0],"%Y-%m-%d %H:%M:%S")
        
        if abs(data_time-now).total_seconds() > 60.:
            raise ValueError("Could not read box temperature")
        else:
            return [float(result[2]),float(result[3]),
                    float(result[4]),float(result[5]),
                    float(result[6]),float(result[7]),
                    float(result[8]),float(result[9]),
                    float(result[10]),float(result[11])]
