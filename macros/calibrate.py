#! /usr/bin/env python3

import os
import shutil
import glob
import math
import array
import sys
import time
import json

import ROOT
import tdrstyle
import numpy as np

from typing import NamedTuple

BAC = "UVA"

good_runs = [
595,
596,
597,
602,
604,
607,
609,
610,
611,
612,
613,
615,
618,
619,
629,
630,
631,
633,
634,
637,
640,
641,
642,
643,
644,
648,
649,
653,
654,
660,
662,
663,
666,
667,
668,
669,
671,
673,
674,
675,
676,
677,
678,
679,
689,
690,
692,
693,
694,
695,
697,
698,
699,
700,
701,
712,
713,
714,
715,
716,
717,
726,
727,
731,
732,
735,
736,
737,
738,
739,
740,
741,
742,
743,
744,
748,
749,
750,
751,
752,
753,
772,
773,
774,
775,
776,
778,
779,
780,
781,
783,
790,
793,
796,
797,
799,
800,
803,
804,
805,
806,
807,
811,
812,
817,
818,
819,
820,
821,
822,
823,
825,
826,
827,
828,
829,
830,
831,
832,
833,
834,
835,
836,
837,
838,
839,
840,
841,
842,
844,
848,
849,
850,
853,
854,
855,
859,
860,
861,
862,
863,
864,
865,
866,
867,
868,
869,
870,
871,
872,
873,
875,
879,
880,
881,
882,
883,
884,
885,
886,
887,
888,
890,
891,
892,
893,
894,
895,
896,
897,
899,
900,
901,
903,
904,
905,
906,
907,
908,
909,
910,
911,
912,
913,
914,
915,
916,
917,
918,
919,
920,
#922,
923,
924,
925,
926,
927,
928,
929,
933,
935,
936,
937,
938,
939,
941,
943,              
944,
]

if BAC == "Milano":
    data_path = '/data1/SMQAQC/PRODUCTION/'
    selections = ['GOOD']
    plotDir = '/data1/html/data1/SMQAQC/PRODUCTION/calibrationPlots_run0050-run0056_calib/'
    #plotDir = '/data1/html/data1/SMQAQC/PRODUCTION/calibrationPlots_run0057-run0062/'
elif BAC == "UVA":
    data_path = '/home/qaqcbtl/qaqc_jig/data/production_copy/'
    selections = ['GOOD']
    plotDir = '/var/www/html/data/production_copy/calibrationPlots_run0595-run0944_calib/'


if not os.path.isdir(plotDir):
    os.mkdir(plotDir)




#set the tdr style
tdrstyle.setTDRStyle()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)
ROOT.gStyle.SetTitleOffset(1.25,'Y')
ROOT.gErrorIgnoreLevel = ROOT.kWarning;
ROOT.gROOT.SetBatch(True)
#ROOT.gROOT.SetBatch(False)

def GetMeanRMS(graph):
    htemp = ROOT.TH1F('htemp','',100,0.,10000)
    for point in range(graph.GetN()):
        #if graph.GetPointY(point) > 1000. and  graph.GetPointY(point) < 5000.:
        htemp.Fill(graph.GetPointY(point))
    return (htemp.GetMean(),htemp.GetRMS())




modules = []
params = {}
inputFiles = glob.glob(data_path+'/run*/*_analysis.root')
for inputFile in inputFiles:
    tokens = inputFile.split('/')
    run = ''
    for token in tokens:
        if 'module' in token:
            module = token[7:21]
        if 'run' in token:
            run = int(token[3:])
    
    if run not in good_runs:
        continue

    jsonFileName = data_path+'run%04d/qaqc_gui.settings'%run
    config = json.load(open(jsonFileName))
    slot = 0
    for barcode in config['barcodes']:
        if barcode == module and config['module_available'][slot] == 1:
            break
        else:
            slot += 1
    modules.append((module,run))
    params[(module,run)] = [inputFile,slot,'GOOD']
    print(module,run,params[(module,run)],config)

bad_modules = [
   "32110020005634",
   "32110020005775",
   "32110020005841",
   "32110020005910",
   "32110020005991",
   "32110020006036",
   "32110020006045",
   "32110020006052",
   "32110020006095",
   "32110020006124",
   "32110020006125",
   "32110020006147",
   "32110020006209",
   "32110020006211",
   "32110020006217",
   "32110020006268",
   "32110020006271",
   "32110020006284",
   "32110020006346",
   "32110020006401",
   "32110020006408",
   "32110020006427",
   "32110020006457",
   "32110020006482",
   "32110020006492",
   "32110020006500",
   "32110020006585",
   "32110020006629",
   "32110020006829",
   "32110020006886",
   "32110020007110",
   "32110020007112",
   "32110020007133",
   "32110020007206",
   "32110020007296",
   "32110020007352",
   "32110020007360",
   "32110020007362",
   "32110020007374",
   "32110020007385",
   "32110020007388",
   "32110020007393",
   "32110020007402",
   "32110020007451",
   "32110020007521",
   "32110020007525",
   "32110020007593",
   "32110020007597",
   "32110020007603",
   "32110020007607",
   "32110020007632",
   "32110020007634",
   "32110020007662",
   "32110020007677",
   "32110020007694",
   "32110020007707",
   "32110020007745",
   "32110020007750",
   "32110020007853",
   "32110020007925",
   "32110020007929",
   "32110020007936",
   "32110020007941",
   "32110020007992",
   "32110020008000",
   "32110020008003",
   "32110020008006",
   "32110020008067",
   "32110020008100",
   "32110020008112",
   "32110020008129",
   "32110020008162",
   "32110020008199",
   "32110020005814",
   "32110020005995",
   "32110020006035",
   "32110020006121",
   "32110020006167",
   "32110020006178",
   "32110020006206",
   "32110020006425",
   "32110020006430",
   "32110020006441",
   "32110020006483",
   "32110020006494",
   "32110020006551",
   "32110020006602",
   "32110020006826",
   "32110020006891",
   "32110020006939",
   "32110020006964",
   "32110020007072",
   "32110020007087",
   "32110020007165",
   "32110020007191",
   "32110020007200",
   "32110020007230",
   "32110020007275",
   "32110020007281",
   "32110020007322",
   "32110020007366",
   "32110020007387",
   "32110020007396",
   "32110020007544",
   "32110020007561",
   "32110020007567",
   "32110020007596",
   "32110020007614",
   "32110020007639",
   "32110020007673",
   "32110020007897",
   "32110020007934",
   "32110020007939",
   "32110020008005",
   "32110020008096",
   "32110020008123",
   "32110020008124",
   "32110020008127",
   "32110020008213",
   "32110020005631",
   "32110020005651",
   "32110020005724",
   "32110020005736",
   "32110020005746",
   "32110020005748",
   "32110020005749",
   "32110020005795",
   "32110020005798",
   "32110020005811",
   "32110020005818",
   "32110020005819",
   "32110020005836",
   "32110020005857",
   "32110020006077",
   "32110020006146",
   "32110020006272",
   "32110020006591",
   "32110020006593",
   "32110020006594",
   "32110020006633",
   "32110020007289",
   "32110020007649",
   "32110020007651",
   "32110020007655",
   "32110020005630",
   "32110020005654",
   "32110020005723",
   "32110020005726",
   "32110020005739",
   "32110020005757",
   "32110020005783",
   "32110020005784",
   "32110020005822",
   "32110020005984",
   "32110020005992",
   "32110020006034",
   "32110020006057",
   "32110020006058",
   "32110020006162",
   "32110020006227",
   "32110020006273",
   "32110020006294",
   "32110020006297",
   "32110020006306",
   "32110020006333",
   "32110020006334",
   "32110020006453",
   "32110020006454",
   "32110020006466",
   "32110020006486",
   "32110020006530",
   "32110020006560",
   "32110020006632",
   "32110020006663",
   "32110020006664",
   "32110020006716",
   "32110020006768",
   "32110020006789",
   "32110020006825",
   "32110020006839",
   "32110020006899",
   "32110020006910",
   "32110020006930",
   "32110020007017",
   "32110020007053",
   "32110020007114",
   "32110020007125",
   "32110020007162",
   "32110020007164",
   "32110020007166",
   "32110020007182",
   "32110020007197",
   "32110020007198",
   "32110020007202",
   "32110020007205",
   "32110020007209",
   "32110020007210",
   "32110020007221",
   "32110020007226",
   "32110020007253",
   "32110020007254",
   "32110020007255",
   "32110020007267",
   "32110020007268",
   "32110020007271",
   "32110020007274",
   "32110020007278",
   "32110020007279",
   "32110020007283",
   "32110020007284",
   "32110020007286",
   "32110020007288",
   "32110020007299",
   "32110020007307",
   "32110020007312",
   "32110020007314",
   "32110020007320",
   "32110020007324",
   "32110020007327",
   "32110020007341",
   "32110020007365",
   "32110020007367",
   "32110020007369",
   "32110020007375",
   "32110020007448",
   "32110020007490",
   "32110020007493",
   "32110020007507",
   "32110020007573",
   "32110020007574",
   "32110020007601",
   "32110020007612",
   "32110020007620",
   "32110020007646",
   "32110020007648",
   "32110020007654",
   "32110020007658",
   "32110020007703",
   "32110020007713",
   "32110020007753",
   "32110020007785",
   "32110020007795",
   "32110020007826",
   "32110020007848",
   "32110020007859",
   "32110020007877",
   "32110020007878",
   "32110020007905",
   "32110020007938",
   "32110020007994",
   "32110020008001",
   "32110020008011",
   "32110020008028",
   "32110020008059",
   "32110020008085",
   "32110020008089",
   "32110020008094",
   "32110020008095",
   "32110020008133",
   "32110020008152",
   "32110020008153",
   "32110020008154",
   "32110020008165",
   "32110020008178",
   "32110020008189",
                                                   
]

#bad_modules.append('32110020006393')
#bad_modules.append('32110020006381')
#bad_modules.append('32110020006370')
#bad_modules.append('32110020006369')
#bad_modules.append('32110020006227')
#bad_modules.append('32110020006441')
#bad_modules.append('32110020006450')
#bad_modules.append('32110020006491')
#bad_modules.append('32110020006450')
#bad_modules.append('32110020006386')
#bad_modules.append('32110020006387')
#bad_modules.append('32110020000009')
#bad_modules.append('32110020000018')
#bad_modules.append('32110020000022')
#bad_modules.append('32110020000024')
#bad_modules.append('32110020000025')
#bad_modules.append('32110020000026')
#bad_modules.append('32110020000034')
#bad_modules.append('32110020000035')
#bad_modules.append('32110020000037')
#bad_modules.append('32110020000040')




p_spe_L_vs_slot = ROOT.TProfile('p_spe_L_vs_slot','',12,-0.5,11.5)
p_spe_R_vs_slot = ROOT.TProfile('p_spe_R_vs_slot','',12,-0.5,11.5)
p_spe_vs_ampli = ROOT.TProfile('p_spe_vs_ampli','',16,-0.5,15.5)

p_lyso_L_vs_slot = ROOT.TProfile('p_lyso_L_vs_slot','',12,-0.5,11.5)
p_lyso_R_vs_slot = ROOT.TProfile('p_lyso_R_vs_slot','',12,-0.5,11.5)
p_lyso_vs_ampli = ROOT.TProfile('p_lyso_vs_ampli','',16,-0.5,15.5)


print('***** spe *****')
for key in modules:
    module = key[0]
    run = key[1]
    param = params[key]
    slot = param[1]
    accept = 1
    #for selection in selections:
    #    tempAccept = 0
    #    for param in params[module]:
    #        if selection in param:
    #            tempAccept = 1
    #    accept *= tempAccept
    if run not in good_runs:
        accept = 0
    if accept == 0:
        continue
    print(module,run,param)
    
    rootfile = ROOT.TFile(params[(module,run)][0],'READ')
    
    graph = rootfile.Get('g_spe_L_raw_vs_bar')
    mean = GetMeanRMS(graph)[0]
    p_spe_L_vs_slot.Fill(slot,mean)
    
    graph = rootfile.Get('g_spe_R_raw_vs_bar')
    mean = GetMeanRMS(graph)[0]
    p_spe_R_vs_slot.Fill(slot,mean)
    
    graph = rootfile.Get('g_spe_raw_vs_ch')
    mean = GetMeanRMS(graph)[0]
    for point in range(graph.GetN()):
        ch = graph.GetPointX(point)
        if ch < 16:
            p_spe_vs_ampli.Fill(ch%8,graph.GetPointY(point)/mean)
        else:
            p_spe_vs_ampli.Fill(15-ch%8,graph.GetPointY(point)/mean)


print('***** lyso *****')
for key in modules:
    module = key[0]
    run = key[1]
    param = params[key]
    slot = param[1]
    accept = 1
    #for selection in selections:
    #    tempAccept = 0
    #    for param in params[module]:
    #        if selection in param:
    #            tempAccept = 1
    #    accept *= tempAccept
    if module in bad_modules:
        accept = 0
    if run not in good_runs:
        accept = 0
    if accept == 0:
        continue
    print(module,run,param)
    
    rootfile = ROOT.TFile(params[(module,run)][0],'READ')
    
    graph = rootfile.Get('g_lyso_L_pc_per_kev_raw_vs_bar')
    mean = GetMeanRMS(graph)[0]
    p_lyso_L_vs_slot.Fill(slot,mean)
    
    graph = rootfile.Get('g_lyso_R_pc_per_kev_raw_vs_bar')
    mean = GetMeanRMS(graph)[0]
    p_lyso_R_vs_slot.Fill(slot,mean)
    
    graph = rootfile.Get('g_lyso_pc_per_kev_raw_vs_ch')
    #mean = GetMeanRMS(graph)[0]
    #values = [graph.GetPointY(x) for x in graph.GetPointX]if (graph.GetPointY(x) <= 2.5 & graphx>=1.5)]
    #good_values =[]
    #good_index =[]
    #for x  in range(len(values))
    #   if (values[x] <= 2.5) and (values[x]>=1.5):
    #       good_values.append(values[x])
    #       good_index.append(x)
    #mean = np.mean(good_values)
    good_points_X = []
    good_points_Y = []
    for point in range(graph.GetN()):
        X = graph.GetPointX(point)
        Y = graph.GetPointY(point)
        if Y  >=1.5 or Y <=2.5:
           good_points_X.append(X)
           good_points_Y.append(Y)
        else:
           print(X,Y)
    mean = np.mean(good_points_Y)
        
        
    for x, y in zip(good_points_X, good_points_Y):
        if x < 16:
            p_lyso_vs_ampli.Fill(x%8,y/mean)
        else:
            p_lyso_vs_ampli.Fill(15-x%8,y/mean)

profiles = [
    p_spe_L_vs_slot,
    p_spe_R_vs_slot,
    p_spe_vs_ampli,
    p_lyso_L_vs_slot,
    p_lyso_R_vs_slot,
    p_lyso_vs_ampli,
]

for prof in profiles:
    print(f"\n=== {prof.GetName()} ===")
    nbins = prof.GetNbinsX()
    for i in range(1, nbins + 1):
        x = prof.GetBinCenter(i)
        y = prof.GetBinContent(i)
        err = prof.GetBinError(i)
        print(f"Bin {i:2d} | x = {x:6.2f} | mean = {y:8.4f} ± {err:6.4f}")


c = ROOT.TCanvas('c_spe_vs_slot','',800,700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
p_spe_L_vs_slot.Scale(1./p_spe_L_vs_slot.GetBinContent(p_spe_L_vs_slot.FindBin(2.)))
p_spe_R_vs_slot.Scale(1./p_spe_R_vs_slot.GetBinContent(p_spe_R_vs_slot.FindBin(2.)))
p_spe_L_vs_slot.SetTitle(';slot;spe charge [a.u.]')
p_spe_L_vs_slot.GetYaxis().SetRangeUser(0.90,1.10)
p_spe_L_vs_slot.SetMarkerStyle(20)
p_spe_L_vs_slot.SetMarkerSize(1.2)
p_spe_L_vs_slot.SetMarkerColor(ROOT.kRed)
p_spe_L_vs_slot.SetLineColor(ROOT.kRed)
p_spe_L_vs_slot.Draw()
p_spe_R_vs_slot.SetMarkerStyle(20)
p_spe_R_vs_slot.SetMarkerSize(1.2)
p_spe_R_vs_slot.SetMarkerColor(ROOT.kBlue)
p_spe_R_vs_slot.SetLineColor(ROOT.kBlue)
p_spe_R_vs_slot.Draw('same')
c.Print('%s/h_spe_LR_slot.png'%plotDir)


c = ROOT.TCanvas('c_spe_vs_ampli','',800,700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
p_spe_vs_ampli.SetTitle(';amplifier channel;a.u.')
p_spe_vs_ampli.GetYaxis().SetRangeUser(0,2)
p_spe_vs_ampli.Draw()
c.Print('%s/h_spe_LR_ch.png'%plotDir)




c = ROOT.TCanvas('c_lyso_vs_slot','',800,700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
p_lyso_L_vs_slot.Scale(1./p_lyso_L_vs_slot.GetBinContent(p_lyso_L_vs_slot.FindBin(2.)))
p_lyso_R_vs_slot.Scale(1./p_lyso_R_vs_slot.GetBinContent(p_lyso_R_vs_slot.FindBin(2.)))
p_lyso_L_vs_slot.SetTitle(';slot;lyso charge [a.u.]')
p_lyso_L_vs_slot.GetYaxis().SetRangeUser(0.90,1.10)
p_lyso_L_vs_slot.SetMarkerStyle(20)
p_lyso_L_vs_slot.SetMarkerSize(1.2)
p_lyso_L_vs_slot.SetMarkerColor(ROOT.kRed)
p_lyso_L_vs_slot.SetLineColor(ROOT.kRed)
p_lyso_L_vs_slot.Draw()
p_lyso_R_vs_slot.SetMarkerStyle(20)
p_lyso_R_vs_slot.SetMarkerSize(1.2)
p_lyso_R_vs_slot.SetMarkerColor(ROOT.kBlue)
p_lyso_R_vs_slot.SetLineColor(ROOT.kBlue)
p_lyso_R_vs_slot.Draw('same')
c.Print('%s/h_lyso_LR_slot.png'%plotDir)


c = ROOT.TCanvas('c_lyso_vs_ampli','',800,700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
p_lyso_vs_ampli.SetTitle(';amplifier channel;a.u.')
p_lyso_vs_ampli.GetYaxis().SetRangeUser(0,2)
p_lyso_vs_ampli.Draw()
c.Print('%s/h_lyso_LR_ch.png'%plotDir)



outfile = ROOT.TFile('%s/calibrate.root'%plotDir,'RECREATE')
outfile.cd()
p_spe_L_vs_slot.Write()
p_spe_R_vs_slot.Write()
p_spe_vs_ampli.Write()
p_lyso_L_vs_slot.Write()
p_lyso_R_vs_slot.Write()
p_lyso_vs_ampli.Write()
outfile.Close()
