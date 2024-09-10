#! /usr/bin/env python3

import os
import shutil
import glob
import math
import array
import sys
import time

import ROOT
import tdrstyle

#from typing import NamedTuple


data_path = '/home/qaqcbtl/qaqc_jig/data/production/'
selections = []
plotDir = '/home/qaqcbtl/qaqc_jig/data/production/summaryPlots_26_SMs_calib/'


#set the tdr style
tdrstyle.setTDRStyle()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)
ROOT.gStyle.SetTitleOffset(1.25,'Y')
ROOT.gErrorIgnoreLevel = ROOT.kWarning;
ROOT.gROOT.SetBatch(True)
#ROOT.gROOT.SetBatch(False)

def GetMaxVar(graph):
    minVal = 999999.
    maxVal = -999999.
    for point in range(graph.GetN()):
        if graph.GetPointY(point) < minVal:
            minVal = graph.GetPointY(point)
        if graph.GetPointY(point) > maxVal:
            maxVal = graph.GetPointY(point)            
    return maxVal-minVal


def GetMeanRMS(graph):
    htemp = ROOT.TH1F('htemp','',100,-100.,10000)
    for point in range(graph.GetN()):
        #if graph.GetPointY(point) > 1000. and  graph.GetPointY(point) < 5000.:
        htemp.Fill(graph.GetPointY(point))
    return (htemp.GetMean(),htemp.GetRMS())

def GetMeanRMS_abs(graph):
    htemp = ROOT.TH1F('htemp','',100,-100.,10000)
    for point in range(graph.GetN()):
        #if graph.GetPointY(point) > 1000. and  graph.GetPointY(point) < 5000.:
        htemp.Fill(abs(graph.GetPointY(point)))
    return (htemp.GetMean(),htemp.GetRMS())


modules = []
params = {}

# retrieving root files 
inputFiles = glob.glob(data_path+'/run*/*_analysis.root')
for inputFile in inputFiles:
    tokens = inputFile.split('/')
    run = ''
    for token in tokens:
        if 'module' in token:
            module = token[7:21] # SM ID
        if 'run' in token:
            run = int(token[3:]) # run number
    modules.append(module)
    params[module] = [inputFile,run,'GOOD']
#print(modules)

if not os.path.isdir(plotDir):
    os.mkdir(plotDir)

# creating histos
h_spe_L_ch = ROOT.TH1F('h_spe_L_ch','',100,3.,5.)
h_spe_R_ch = ROOT.TH1F('h_spe_R_ch','',100,3.,5.)

h_LO_avg_bar = ROOT.TH1F('h_LO_avg_bar','',100,1200.,5200.)
h_LO_L_bar = ROOT.TH1F('h_LO_L_bar','',100,1200.,5200.)
h_LO_R_bar = ROOT.TH1F('h_LO_R_bar','',100,1200.,5200.)
h_LO_asymm_bar = ROOT.TH1F('h_LO_asymm_bar','',100,0,0.2)

h_LO_avg_ch = ROOT.TH1F('h_LO_avg_ch','',100,1200.,5200.)
h_LO_L_ch = ROOT.TH1F('h_LO_L_ch','',100,1200.,5200.)
h_LO_R_ch = ROOT.TH1F('h_LO_R_ch','',100,1200.,5200.)
h_LO_asymm_ch = ROOT.TH1F('h_LO_asymm_ch','',100,-0.4,0.4)

h_LOrms_bar = ROOT.TH1F('h_LOrms_bar','',60,0.,30.)
h_LOrms_ch = ROOT.TH1F('h_LOrms_ch','',60,0.,30.)

h_LOmaxvar_bar = ROOT.TH1F('h_LOmaxvar_bar','',50,0.,100.)
h_LOmaxvar_ch = ROOT.TH1F('h_LOmaxvar_ch','',50,0.,100.)


# selecting the modules to be included in the summary: accept 1 if included, 0 otherwise
for module in modules:
    param = params[module]
    accept = 1
    if param[1] < 50: # measurements re-done after changing module boards
        accept = 0 
    elif param[1] > 56 and param[1] < 63: # uniformity tests
        accept = 0 
    elif param[1]>67:
        accept = 0
    
    #for selection in selections:
    #    tempAccept = 0
    #    for param in params:
    #        if selection in param:
    #            tempAccept = 1
    #    accept *= tempAccept
    if accept == 0:
        continue
    
    print("analyzing ", module,"    --> ",param)
    
    
    rootfile = ROOT.TFile(params[module][0],'READ')
    
    # filling histos
    graph = rootfile.Get('g_spe_L_vs_bar')
    for point in range(graph.GetN()):
        h_spe_L_ch.Fill(graph.GetPointY(point))
    
    graph = rootfile.Get('g_spe_R_vs_bar')
    for point in range(graph.GetN()):
        h_spe_R_ch.Fill(graph.GetPointY(point))
            
    graph = rootfile.Get('g_avg_light_yield_vs_bar')
    h_LO_avg_bar.Fill(GetMeanRMS(graph)[0])
    h_LOrms_bar.Fill(GetMeanRMS(graph)[1]/GetMeanRMS(graph)[0]*100.)
    h_LOmaxvar_bar.Fill(GetMaxVar(graph)/GetMeanRMS(graph)[0]*100.)
    for point in range(graph.GetN()):
        h_LO_avg_ch.Fill(graph.GetPointY(point))
    
    graph = rootfile.Get('g_light_yield_asymm_vs_bar')
    h_LO_asymm_bar.Fill(GetMeanRMS_abs(graph)[0])
    for point in range(graph.GetN()):
        h_LO_asymm_ch.Fill(graph.GetPointY(point))
            
    graph = rootfile.Get('g_L_light_yield_vs_bar')
    h_LO_L_bar.Fill(GetMeanRMS(graph)[0])
    for point in range(graph.GetN()):
        h_LO_L_ch.Fill(graph.GetPointY(point))

    graph = rootfile.Get('g_R_light_yield_vs_bar')
    h_LO_R_bar.Fill(GetMeanRMS(graph)[0])
    for point in range(graph.GetN()):
        h_LO_R_ch.Fill(graph.GetPointY(point))

    graph = rootfile.Get('g_light_yield_vs_ch')
    h_LOrms_ch.Fill(GetMeanRMS(graph)[1]/GetMeanRMS(graph)[0]*100.)
    h_LOmaxvar_ch.Fill(GetMaxVar(graph)/GetMeanRMS(graph)[0]*100.)




# draw histos

c = ROOT.TCanvas('c_spe_LR_ch','',800,700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
h_spe_L_ch.SetTitle(';single p.e. charge [pC];entries')
h_spe_L_ch.SetFillStyle(3001)
h_spe_L_ch.SetFillColor(ROOT.kRed)
h_spe_L_ch.SetLineColor(ROOT.kRed)
h_spe_L_ch.GetYaxis().SetRangeUser(0.,1.1*max(h_spe_L_ch.GetMaximum(),h_spe_R_ch.GetMaximum()))
h_spe_L_ch.Draw()
latex_L = ROOT.TLatex(0.64,0.70,'#splitline{mean: %.2e}{RMS: %.1f %%}'%(h_spe_L_ch.GetMean(),h_spe_L_ch.GetRMS()/h_spe_L_ch.GetMean()*100.))
latex_L.SetNDC()
latex_L.SetTextSize(0.05)
latex_L.SetTextColor(ROOT.kRed)
latex_L.Draw('same')
h_spe_R_ch.SetFillStyle(3001)
h_spe_R_ch.SetFillColor(ROOT.kBlue)
h_spe_R_ch.SetLineColor(ROOT.kBlue)
h_spe_R_ch.Draw('same')
latex_R = ROOT.TLatex(0.64,0.40,'#splitline{mean: %.2e}{RMS: %.1f %%}'%(h_spe_R_ch.GetMean(),h_spe_R_ch.GetRMS()/h_spe_R_ch.GetMean()*100.))
latex_R.SetNDC()
latex_R.SetTextSize(0.05)
latex_R.SetTextColor(ROOT.kBlue)
latex_R.Draw('same')
c.Print('%s/h_spe_LR_ch.png'%plotDir)




c = ROOT.TCanvas('c_LO_avg_bar','',800,700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
h_LO_avg_bar.SetTitle(';avg. bar light output [pe/MeV];entries')
h_LO_avg_bar.SetFillStyle(3001)
h_LO_avg_bar.SetFillColor(ROOT.kBlack)
h_LO_avg_bar.Draw()
latex = ROOT.TLatex(0.64,0.60,'#splitline{mean: %.2e}{RMS: %.1f %%}'%(h_LO_avg_bar.GetMean(),h_LO_avg_bar.GetRMS()/h_LO_avg_bar.GetMean()*100.))
latex.SetNDC()
latex.SetTextSize(0.05)
latex.Draw('same') 
line_low = ROOT.TLine(0.85*3200.,0.,0.85*3200,1.05*h_LO_avg_bar.GetMaximum())
line_low.SetLineColor(ROOT.kGreen+1)
line_low.SetLineWidth(4)
line_low.SetLineStyle(2)
line_low.Draw('same')
c.Print('%s/h_LO_avg_bar.png'%plotDir)

c = ROOT.TCanvas('c_LO_avg_ch','',800,700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
h_LO_avg_ch.SetTitle(';bar light output [pe/MeV];entries')
h_LO_avg_ch.SetFillStyle(3001)
h_LO_avg_ch.SetFillColor(ROOT.kBlack)
h_LO_avg_ch.Draw()
latex = ROOT.TLatex(0.64,0.60,'#splitline{mean: %.2e}{RMS: %.1f %%}'%(h_LO_avg_ch.GetMean(),h_LO_avg_ch.GetRMS()/h_LO_avg_ch.GetMean()*100.))
latex.SetNDC()
latex.SetTextSize(0.05)
latex.Draw('same')
line_low = ROOT.TLine(0.85*3200.,0.,0.85*3200,1.05*h_LO_avg_ch.GetMaximum())
line_low.SetLineColor(ROOT.kGreen+1)
line_low.SetLineWidth(4)
line_low.SetLineStyle(2)
line_low.Draw('same')
c.Print('%s/h_LO_avg_ch.png'%plotDir)




c = ROOT.TCanvas('c_LO_LR_bar','',800,700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
h_LO_L_bar.SetTitle(';avg. channel light output [pe/MeV];entries')
h_LO_L_bar.SetFillStyle(3001)
h_LO_L_bar.SetFillColor(ROOT.kRed)
h_LO_L_bar.SetLineColor(ROOT.kRed)
h_LO_L_bar.GetYaxis().SetRangeUser(0.,1.1*max(h_LO_L_bar.GetMaximum(),h_LO_R_bar.GetMaximum()))
h_LO_L_bar.Draw()
latex_L = ROOT.TLatex(0.64,0.70,'#splitline{mean: %.2e}{RMS: %.1f %%}'%(h_LO_L_bar.GetMean(),h_LO_L_bar.GetRMS()/h_LO_L_bar.GetMean()*100.))
latex_L.SetNDC()
latex_L.SetTextSize(0.05)
latex_L.SetTextColor(ROOT.kRed)
latex_L.Draw('same')
h_LO_R_bar.SetFillStyle(3001)
h_LO_R_bar.SetFillColor(ROOT.kBlue)
h_LO_R_bar.SetLineColor(ROOT.kBlue)
h_LO_R_bar.Draw('same')
latex_R = ROOT.TLatex(0.64,0.40,'#splitline{mean: %.2e}{RMS: %.1f %%}'%(h_LO_R_bar.GetMean(),h_LO_R_bar.GetRMS()/h_LO_R_bar.GetMean()*100.))
latex_R.SetNDC()
latex_R.SetTextSize(0.05)
latex_R.SetTextColor(ROOT.kBlue)
latex_R.Draw('same')
line_low = ROOT.TLine(0.85*3200.,0.,0.85*3200.,1.*max(h_LO_L_bar.GetMaximum(),h_LO_R_bar.GetMaximum()))
line_low.SetLineColor(ROOT.kGreen+1)
line_low.SetLineWidth(4)
line_low.SetLineStyle(2)
line_low.Draw('same')
c.Print('%s/h_LO_LR_bar.png'%plotDir)

c = ROOT.TCanvas('c_LO_LR_ch','',800,700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
h_LO_L_ch.SetTitle(';channel light output [pe/MeV];entries')
h_LO_L_ch.SetFillStyle(3001)
h_LO_L_ch.SetFillColor(ROOT.kRed)
h_LO_L_ch.SetLineColor(ROOT.kRed)
h_LO_L_ch.GetYaxis().SetRangeUser(0.,1.1*max(h_LO_L_ch.GetMaximum(),h_LO_R_ch.GetMaximum()))
h_LO_L_ch.Draw()
latex_L = ROOT.TLatex(0.64,0.70,'#splitline{mean: %.2e}{RMS: %.1f %%}'%(h_LO_L_ch.GetMean(),h_LO_L_ch.GetRMS()/h_LO_L_ch.GetMean()*100.))
latex_L.SetNDC()
latex_L.SetTextSize(0.05)
latex_L.SetTextColor(ROOT.kRed)
latex_L.Draw('same')
h_LO_R_ch.SetFillStyle(3001)
h_LO_R_ch.SetFillColor(ROOT.kBlue)
h_LO_R_ch.SetLineColor(ROOT.kBlue)
h_LO_R_ch.Draw('same')
latex_R = ROOT.TLatex(0.64,0.40,'#splitline{mean: %.2e}{RMS: %.1f %%}'%(h_LO_R_ch.GetMean(),h_LO_R_ch.GetRMS()/h_LO_R_ch.GetMean()*100.))
latex_R.SetNDC()
latex_R.SetTextSize(0.05)
latex_R.SetTextColor(ROOT.kBlue)
latex_R.Draw('same')
line_low = ROOT.TLine(0.85*3200.,0.,0.85*3200.,1.*max(h_LO_L_ch.GetMaximum(),h_LO_R_ch.GetMaximum()))
line_low.SetLineColor(ROOT.kGreen+1)
line_low.SetLineWidth(4)
line_low.SetLineStyle(2)
line_low.Draw('same')
c.Print('%s/h_LO_LR_ch.png'%plotDir)




c = ROOT.TCanvas('c_LO_asymm_bar','',800,700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
h_LO_asymm_bar.SetTitle(';avg. L.O. asymmetry [ 2*(L-R)/(L+R) ];entries')
h_LO_asymm_bar.SetFillStyle(3001)
h_LO_asymm_bar.SetFillColor(ROOT.kBlack)
h_LO_asymm_bar.Draw()
latex = ROOT.TLatex(0.64,0.60,'#splitline{mean: %.2e}{RMS: %.1f %%}'%(h_LO_asymm_bar.GetMean(),h_LO_asymm_bar.GetRMS()*100.))
latex.SetNDC()
latex.SetTextSize(0.05)
latex.Draw('same') 
# line_low = ROOT.TLine(-0.1,0.,-0.1,1.05*h_LO_asymm_bar.GetMaximum())
# line_low.SetLineColor(ROOT.kGreen+1)
# line_low.SetLineWidth(4)
# line_low.SetLineStyle(2)
# line_low.Draw('same')
line_high = ROOT.TLine(0.1,0.,0.1,1.05*h_LO_asymm_bar.GetMaximum())
line_high.SetLineColor(ROOT.kGreen+1)
line_high.SetLineWidth(4)
line_high.SetLineStyle(2)
line_high.Draw('same')
c.Print('%s/h_LO_asymm_bar.png'%plotDir)

c = ROOT.TCanvas('c_LO_asymm_ch','',800,700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
h_LO_asymm_ch.SetTitle(';L.O. asymmetry [ 2*(L-R)/(L+R) ];entries')
h_LO_asymm_ch.SetFillStyle(3001)
h_LO_asymm_ch.SetFillColor(ROOT.kBlack)
h_LO_asymm_ch.Draw()
latex = ROOT.TLatex(0.64,0.60,'#splitline{mean: %.2e}{RMS: %.1f %%}'%(h_LO_asymm_ch.GetMean(),h_LO_asymm_ch.GetRMS()*100.))
latex.SetNDC()
latex.SetTextSize(0.05)
latex.Draw('same') 
line_low = ROOT.TLine(-0.2,0.,-0.2,1.05*h_LO_asymm_ch.GetMaximum())
line_low.SetLineColor(ROOT.kGreen+1)
line_low.SetLineWidth(4)
line_low.SetLineStyle(2)
line_low.Draw('same')
line_high = ROOT.TLine(0.2,0.,0.2,1.05*h_LO_asymm_ch.GetMaximum())
line_high.SetLineColor(ROOT.kGreen+1)
line_high.SetLineWidth(4)
line_high.SetLineStyle(2)
line_high.Draw('same')
c.Print('%s/h_LO_asymm_ch.png'%plotDir)




c = ROOT.TCanvas('c_LOrms_bar','',800,700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
h_LOrms_bar.SetTitle(';bar RMS [%];entries')
h_LOrms_bar.SetFillStyle(3001)
h_LOrms_bar.SetFillColor(ROOT.kBlack)
h_LOrms_bar.Draw()
line = ROOT.TLine(5.,0.,5.,1.05*h_LOrms_bar.GetMaximum())
line.SetLineColor(ROOT.kGreen+1)
line.SetLineWidth(4)
line.SetLineStyle(2)
line.Draw('same')
c.Print('%s/h_LOrms_bar.png'%plotDir)

c = ROOT.TCanvas('c_LOrms_ch','',800,700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
h_LOrms_ch.SetTitle(';channel RMS [%];entries')
h_LOrms_ch.SetFillStyle(3001)
h_LOrms_ch.SetFillColor(ROOT.kBlack)
h_LOrms_ch.Draw()
line = ROOT.TLine(7.,0.,7.,1.05*h_LOrms_ch.GetMaximum())
line.SetLineColor(ROOT.kGreen+1)
line.SetLineWidth(4)
line.SetLineStyle(2)
line.Draw('same')
c.Print('%s/h_LOrms_ch.png'%plotDir)



c = ROOT.TCanvas('c_LOmaxvar_bar','',800,700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
h_LOmaxvar_bar.SetTitle(';bar max. var. [%];entries')
h_LOmaxvar_bar.SetFillStyle(3001)
h_LOmaxvar_bar.SetFillColor(ROOT.kBlack)
h_LOmaxvar_bar.Draw()
line = ROOT.TLine(30.,0.,30.,1.05*h_LOmaxvar_bar.GetMaximum())
line.SetLineColor(ROOT.kGreen+1)
line.SetLineWidth(4)
line.SetLineStyle(2)
line.Draw('same')
c.Print('%s/h_LOmaxvar_bar.png'%plotDir)

c = ROOT.TCanvas('c_LOmaxvar_ch','',800,700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
h_LOmaxvar_ch.SetTitle(';channel max. var. [%];entries')
h_LOmaxvar_ch.SetFillStyle(3001)
h_LOmaxvar_ch.SetFillColor(ROOT.kBlack)
h_LOmaxvar_ch.Draw()
line = ROOT.TLine(40.,0.,40.,1.05*h_LOmaxvar_ch.GetMaximum())
line.SetLineColor(ROOT.kGreen+1)
line.SetLineWidth(4)
line.SetLineStyle(2)
line.Draw('same')
c.Print('%s/h_LOmaxvar_ch.png'%plotDir)
