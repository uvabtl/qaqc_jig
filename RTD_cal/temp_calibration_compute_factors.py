'''
Calibration of RTD reading due to variations in RTD Readout Electronics
We used a fixed resistor of 1103 Ohms and placed in each SiPM slot. Linearity is assumed, so we determine the scaling factor that needs to be applied to each "temperature" so that it corresponds to the correct temperature readout for 1103 Ohms.
'''

import sys
import re

import numpy as np
import json

def compute_cal_temp(fixed_resistance):
    '''
        Code from firmware - for fixed resistance value we should known what temperature to read out
    '''
    gain = 40
    iref = 100e-6
    r0 = 1000
    r3 = 778.1
    A0 = 3.9083e-3;
    vout = gain*iref*(fixed_resistance - r3)
    r = vout/(gain*iref) + r3;
    return (r/r0 - 1)/A0



if __name__ == '__main__':

    file_loc = sys.argv[1]

    #first, compute the expected temperature readout for the fixed resistor
    #this is directly from the firmware/QAQC manual
    fixed_resistance = float(sys.argv[2])
    cal_temp = compute_cal_temp(fixed_resistance)
    RTD_cal_info = {}
    with open(file_loc, 'r') as file:
        for line in file:
            board_loc = line.index("board")
            board = line[board_loc+len("board = "):(line[board_loc:].find(",")+board_loc)]
            print("board number(0-7):",board)
            position_loc = line.index("board_position")
            position = int(line[position_loc+len("board_position = "):(line[position_loc:].find(",")+position_loc)])
            print("Board position:",position)
            side = line.index("jig_side")
            jig_side = (line[side+len("jig_side = "):(line[side:].find(",")+side)])
            print("front(a) or back(b):",jig_side)
            if jig_side=='a':
                position=0
                position=2-position
            else:
                position==1
            jig_position=line.index("jig_position")
            slot_number= int(line[jig_position+len("slot_number = "):(line[jig_position:].find(",")+jig_position)])
            print("slot_number (0-11):", slot_number)
            temp_str = line[line.index("temperatures")+len("temperatures = "):]
            if "None" in temp_str:
                replacement = temp_str[1:temp_str.find(',')]
                temp_str_mod = re.sub("None", replacement, temp_str_mod)
            else:
                temp_str_mod = temp_str
            temp_array = json.loads(temp_str_mod)
            temp_avg = np.average(temp_array)
           # if temp_avg>30 or temp_avg<20:
               # RTD_cal_info[board]["thermistor " + str(position)] = (None, None)

            
            
            data_key = f"{slot_number}_{jig_side}"
            RTD_cal_info[data_key] = {
                "board_id": board,
                "slot_number": slot_number,
                "front(a)_or_back(b)": jig_side,
                "scale_factor": cal_temp / temp_avg,
                "uncert": cal_temp / temp_avg * (np.std(temp_array) / temp_avg)
            }
 #           RTD_cal_info[str(slot_key)+"_"+str(jig_side)] = ("board id: "+str(board),"slot_number: "+str(slot_number),"front(0) or back(1): "+str(jig_side),"Scale factor: "+str(cal_temp/temp_avg), "uncert: "+str(cal_temp/temp_avg*(np.std(temp_array)/temp_avg)))
    #json_filename ="scale_factor_"+str(board)+"_"+str(slot_number)+"_"+str(jig_side)+".json"
    json_filename ="scale_factor.json"
    with open(json_filename, 'w') as file:
        json.dump(RTD_cal_info, file, indent=4)
