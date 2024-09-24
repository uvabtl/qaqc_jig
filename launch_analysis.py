#! /usr/bin/python3

import os
import argparse

parser = argparse.ArgumentParser(description='Launch reco')
parser.add_argument("-s", "--submit", help="submit jobs", action='store_true')
args = parser.parse_args()

path = './data/production/'
sourceType = 'cesium'

modules = [
    # ('run0087','module_32110020000078','2'),
    # ('run0087','module_32110020000079','3'),
    # ('run0087','module_32110020000080','4'),
    # ('run0087','module_32110020000081','5'),

    #('run0248','module_32110020005601','0'),
    #('run0249','module_32110020005602','1'),
    #('run0249','module_32110020005603','2'),
    #('run0249','module_32110020005604','3'),
    #('run0249','module_32110020005605','4'),
    #('run0249','module_32110020005606','5'),
    #('run0249','module_32110020005607','6'),
    #('run0249','module_32110020005608','7'),
    #('run0249','module_32110020005609','8'),
    #('run0249','module_32110020005610','9'),
    #('run0249','module_32110020005611','10'),
    ('run0356','module_32110020005612','0'),
    ('run0356','module_32110020005613','1'),
    ('run0356','module_32110020005614','2'),
    ('run0356','module_32110020005615','3'),
    ('run0356','module_32110020000041','4'),
    ('run0356','module_32110020005616','5'),
    ('run0356','module_32110020005617','6'),
    ('run0356','module_32110020005618','7'),
    ('run0356','module_32110020005619','8'),
    ('run0356','module_32110020005620','9'),
    ('run0356','module_32110020005621','10'),
    ('run0356','module_32110020005622','11'),

    ('run0358','module_32110020005623','0'),
    ('run0358','module_32110020005624','1'),
    ('run0358','module_32110020005625','2'),
    ('run0358','module_32110020005626','3'),
    ('run0358','module_32110020005627','4'),
    ('run0358','module_32110020005628','5'),
    ('run0358','module_32110020005629','6'),
    ('run0358','module_32110020000041','7'),
    ('run0358','module_32110020005630','8'),
    ('run0358','module_32110020005631','9'),
    ('run0358','module_32110020005632','10'),
    ('run0358','module_32110020005633','11'),

    ('run0359','module_32110020005634','0'),
    ('run0359','module_32110020005635','1'),
    ('run0359','module_32110020005636','2'),
    ('run0359','module_32110020005637','3'),
    ('run0359','module_32110020005638','4'),
    ('run0359','module_32110020005639','5'),
    ('run0359','module_32110020005640','6'),
    ('run0359','module_32110020005641','7'),
    ('run0359','module_32110020005642','8'),
    ('run0359','module_32110020005643','9'),
    ('run0359','module_32110020000041','10'),
    ('run0359','module_32110020005644','11'),

    ('run0360','module_32110020000041','0'),
    ('run0360','module_32110020005637','1'),
    ('run0360','module_32110020005638','2'),
    ('run0360','module_32110020005639','3'),
    ('run0360','module_32110020005640','4'),
    ('run0360','module_32110020005641','5'),
    ('run0360','module_32110020005642','6'),
    ('run0360','module_32110020005643','7'),
    ('run0360','module_32110020005644','8'),
    ('run0360','module_32110020005645','9'),
    ('run0360','module_32110020005646','10'),
    ('run0360','module_32110020005647','11'),

    ('run0361','module_32110020005602','1'),
    ('run0361','module_32110020005603','2'),
    ('run0361','module_32110020005604','3'),
    ('run0361','module_32110020000041','4'),
    ('run0361','module_32110020005605','5'),
    ('run0361','module_32110020005606','6'),
    ('run0361','module_32110020005607','7'),
    ('run0361','module_32110020005608','8'),
    ('run0361','module_32110020005609','9'),
    ('run0361','module_32110020005610','10'),
    ('run0361','module_32110020005611','11'),
]

for module in modules:
    command = 'analyze-waveforms --slot '+module[2]+' --sourceType %s --print-pdfs /var/www/html/ -o %s/%s_analysis.root %s/%s_integrals.hdf5' % (sourceType,path+module[0],module[1],path+module[0],module[1])
    print(command)
    if args.submit: os.system(command)
