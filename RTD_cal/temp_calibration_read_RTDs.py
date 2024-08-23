from btl import Client
import random
import os
import json
import os

import numpy as np
import sys

import time

import logging

DEBUG = False

def print_warning(msg):
    if not msg.endswith('\n'):
        msg += '\n'
    print(msg)

def query(client, cmd):
    print( "%s\n" % cmd)
    if not DEBUG:
        return client.query(cmd)


def poll_single_module_side(client, module, side):
    values = {}
    k = 0 if side == 'a' else 1 
    # Diagram to help figure out what's going on. It's drawn as if you
    # are looking top down at the modules plugged in:
    #
    #     Bus Thermistor Module Bus Thermistor
    #     --- ---------- ------ --- ----------
    #      2      0         5    3      2
    #      2      1         4    3      1
    #      2      2         3    3      0
    #
    #      0      0         2    1      2
    #      0      1         1    1      1
    #      0      2         0    1      0
    bus = (module//3)*2 + k
    thermistor = module % 3

    if k == 0:
        # Ordering for the board on left side is backwards from the
        # board on the right side
        thermistor = 2 - thermistor

    key = '_a' if k == 0 else '_b'

    try:
        thermistor_value = query(client, "thermistor_read %i %i" % (bus, thermistor))
        if DEBUG:
            thermistor_value = random.uniform(20,30)
    except Exception as e:
        print_warning(str(e))
        return

    return thermistor_value


if __name__ == '__main__':

    ip_address = '192.168.0.50' #MAY NEED TO CHANGE
    data_path = '/home/qaqcbtl/qaqc_jig/RTD_cal/' #MAY NEED TO CHANGE
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    client = Client(ip_address)

    board_label = sys.argv[1] #NAME OF BOARD (WE DO CIT_PROD_{BOARD ADDRESS})
    pos = sys.argv[2] #0-11, DEPENDING ON MODULE SLOT 
    side = sys.argv[3] #EITHER a OR b. SIDE a IS CLOSER TO THE USER (EVEN # BOARD ADDRESSES). OTHER SIDE IS b

    poll_rate = 1 #how often to poll temperature in seconds
    num_polls = 10 #number of polls
    
    temp_values = []
    for i in range(num_polls):
        temp_values.append(poll_single_module_side(client, int(pos),side))
        time.sleep(poll_rate)


    LOG_FILENAME = sys.argv[1]+'_'+sys.argv[2]+'_'+sys.argv[3]+'.log'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
    logging.info(f'board = {board_label}, board_position = {int(pos)%3}, jig_position = {pos}, jig_side = {side}, temperatures = {temp_values}')




