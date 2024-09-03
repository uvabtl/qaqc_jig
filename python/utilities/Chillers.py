import os
import sys
from subprocess import Popen, PIPE

BAC = "UVA"

if BAC == "CERN":
    print()
    
if BAC == "Milano":
    sys.path.append('/home/cmsdaq/Programs/Lab5015Utils')
    from Lab5015_utils import LAUDAChiller

if BAC == "UVA":
    sys.path.append('/home/qaqcbtl/Lab5015Utils')
    from Lab5015_utils import PolyScienceChiller


class Chiller:
    def __init__(self):
        if BAC == "Milano":
            self.chiller = LAUDAChiller(portname='tcp://pc-mtd-mib01:5050')
        if BAC == "UVA":
            self.chiller = PolyScienceChiller(portname="/dev/polyscience", verbose=True)
        if BAC == "CERN":
            print()
            
    def getState(self):
        if BAC in ["Milano", "UVA"]:
            state = self.chiller.check_state()
            return state
        if BAC == "CERN":
            print()
    
    def setState(self,state):
        if BAC in ["Milano", "UVA"]:
            self.chiller.set_state(state)
        if BAC == "CERN":
            print()

    def getWaterTemp(self):
        if BAC in ["Milano", "UVA"]:
            temp = self.chiller.read_meas_temp()
            return temp
        if BAC == "CERN":
            print()

    def setTemp(self,temp):
        if BAC in ["Milano", "UVA"]:
            self.chiller.write_set_temp(temp)
        if BAC == "CERN":
            print()
    
    def startPIDProcess(self, temp):
        if BAC == "Milano":
            proc = Popen(['nohup','python3','/home/cmsdaq/DAQ/qaqc_jig/python/utilities/setBoxTemp_PID.py','--target','%f'%temp,'&'])
            return proc
        if BAC == "UVA":
            proc = Popen(['nohup','python3','/home/qaqcbtl/qaqc_jig/python/utilities/setBoxTemp_PID.py','--target','%f'%temp,'&'])
            return proc
        if BAC == "CERN":
            print()

    def stopPIDProcess(self,pid):
        if BAC in ["Milano", "UVA"]:
            os.system('kill -9 %d'%pid)
            self.chiller.set_state('0')
        if BAC == "CERN":
            print()
            
