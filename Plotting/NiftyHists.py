import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)
ROOT.gStyle.SetLegendTextSize(0.1)
canvas = ROOT.TCanvas("NiftyPlotter")
canvas.SetCanvasSize(600,400)
pads = []
pads.append(ROOT.TPad("Nifty1","Nifty1",0,0,0.67,1))
pads.append(ROOT.TPad("Nifty2","Nifty2",0.67,0,1,1))
pads[0].SetTicks(1,2)
pads[0].SetLeftMargin(0.14)
pads[0].SetTopMargin(0.12)
pads[0].SetRightMargin(0.12)
pads[0].Draw()
pads[1].Draw()
pads[0].cd()

ROOT.gStyle.SetLegendBorderSize(0)
legend = ROOT.TLegend(0.0,0.2,0.6,0.8)
legend.SetMargin(0.1)
legend.SetTextSize(0.05)

simplecanvas = ROOT.TCanvas("SimpleNiftyPlotter")
simplecanvas.SetCanvasSize(600,600)
simplecanvas.SetTicks(1,2)
simplecanvas.SetLeftMargin(0.14)
simplecanvas.SetTopMargin(0.12)
simplecanvas.SetRightMargin(0.12)

def HistComp (h):
    return h.Integral()

def OverlayScaledToMax(listOfHists,tags,title=None,save=None,log=False,minimum=0,suppressWarning=False):
    canvas.cd()
    histlist = [h.Clone(h.GetName()+"tmp") for h in listOfHists]
    if tags != None:
        if len(tags) < len(histlist): raise Exception("Not enough tags provided, {0} < {1}".format(len(tags),len(histlist)))
        else:
            if not suppressWarning and len(tags) > len(histlist): print "[NiftyHists] Warning: More tags provided than histograms."
            histdict = dict(zip(histlist,tags))
    else:
        histdict = dict(zip(histlist,[h.GetTitle() for h in histlist]))
    sortedHists = sorted(histlist,key = HistComp,reverse=True)
    if log and minimum == 0: minimum = 0.001
    sortedHists[0].SetMinimum(minimum)
    pads[0].cd()
    NbinsX = sortedHists[0].GetXaxis().GetNbins()
    sortedHists[0].GetXaxis().SetLabelSize(1.0/NbinsX)
    legend.Clear()
    if title != None: sortedHists[0].SetTitle(title)
    sortedHists[0].Draw("E")
    legend.AddEntry(sortedHists[0],histdict[sortedHists[0]])
    for h in sortedHists[1:]:
        if (h.Integral() > 0):
            rescale = int(sortedHists[0].Integral() / h.Integral() )
        else:
            rescale = 1
        h.Scale(rescale)
        if rescale > 1:
            legend.AddEntry(h,histdict[h] + " x " + str(rescale))
        else: 
            legend.AddEntry(h,histdict[h])
        h.Draw("sameE")
    pads[1].cd()
    pads[0].SetLogy(log)
    if save != None: canvas.SaveAs(save)

def OverlayScaledToMin(listOfHists,tags,title=None,save=None,log=False,minimum=0,suppressWarning=False):
    canvas.cd()
    histlist = [h.Clone(h.GetName()+"tmp") for h in listOfHists]
    if tags != None:
        if len(tags) < len(histlist): raise Exception("Not enough tags provided, {0} < {1}".format(len(tags),len(histlist)))
        else:
            if not suppressWarning and len(tags) > len(histlist): print "[NiftyHists] Warning: More tags provided than histograms."
            histdict = dict(zip(histlist,tags))
    else:
        histdict = dict(zip(histlist,[h.GetTitle() for h in histlist]))
    sortedHists = sorted(histlist,key = HistComp,reverse=False)
    if log and minimum == 0: minimum = 0.001
    sortedHists[0].SetMinimum(minimum)
    labelSize = histlist[0].GetXaxis().GetLabelSize()
    NbinsX = histlist[0].GetXaxis().GetNbins()
    sortedHists[0].GetXaxis().SetLabelSize(min(1.0/NbinsX,labelSize))
    if title != None: sortedHists[0].SetTitle(title)
    pads[0].cd()
    legend.Clear()
    sortedHists[0].Draw("E")
    legend.AddEntry(sortedHists[0],histdict[sortedHists[0]])
    for h in sortedHists[1:]:
        if (h.Integral() > 0):
            rescale = int(h_integral() / sortedHists[0].Integral())            
        else:
            rescale = 1
        h.Scale(1.0 / rescale)
        if rescale > 1:
            legend.AddEntry(h,histdict[h] + " x 1/" + str(rescale))
        else: 
            legend.AddEntry(h,histdict[h])
        h.Draw("sameE")
    pads[1].cd()
    legend.Draw()
    pads[0].SetLogy(log)
    if save != None: canvas.SaveAs(save)

def OverlayUnitArea(listOfHists,tags,title=None,save=None,log=False,minimum=0,suppressWarning=False):
    canvas.cd()
    histlist = [h.Clone(h.GetName()+"tmp") for h in listOfHists]
    if tags != None:
        if len(tags) < len(histlist): raise Exception("Not enough tags provided, {0} < {1}".format(len(tags),len(histlist)))
        else:
            if not suppressWarning and len(tags) > len(histlist): print "[NiftyHists] Warning: More tags provided than histograms."
            histdict = dict(zip(histlist,tags))
    else:
        histdict = dict(zip(histlist,[h.GetTitle() for h in histlist]))
    legend.Clear()
    for h in histlist:
        integral = int(h.Integral())
        if integral > 0:
            h.Scale(1.0 / integral)
        legend.AddEntry(h,histdict[h] + " (" + str(integral) + ")")
    histlist[0].SetMaximum(1.2 * max([h.GetMaximum() for h in histlist]))    
    if log and minimum == 0: minimum = 0.001
    histlist[0].SetMinimum(minimum)
    labelSize = histlist[0].GetXaxis().GetLabelSize()
    NbinsX = histlist[0].GetXaxis().GetNbins()
    histlist[0].GetXaxis().SetLabelSize(min(1.0/NbinsX,labelSize))
    if title != None: histlist[0].SetTitle(title)
    pads[0].cd()
    histlist[0].Draw("E")
    for h in histlist[1:]:
        h.Draw("sameE")
    pads[1].cd()
    legend.Draw()
    pads[0].SetLogy(log)
    if save != None: canvas.SaveAs(save)

def Overlay(listOfHists,tags,title=None,save=None,log=False,minimum=0,suppressWarning=False):
    canvas.cd()
    histlist = [h.Clone(h.GetName()+"tmp") for h in listOfHists]
    if tags != None:
        if len(tags) < len(histlist): raise Exception("Not enough tags provided, {0} < {1}".format(len(tags),len(histlist)))
        else:
            if not suppressWarning and len(tags) > len(histlist): print "[NiftyHists] Warning: More tags provided than histograms. {0}, {1}".format(len(tags),len(histlist))
            histdict = dict(zip(histlist,tags))
    else:
        histdict = dict(zip(histlist,[h.GetTitle() for h in histlist]))
    legend.Clear()
    for h in histlist:
        legend.AddEntry(h,histdict[h])
    histlist[0].SetMaximum(1.2 * max([h.GetMaximum() for h in histlist]))
    if log and minimum == 0: minimum = 0.001
    histlist[0].SetMinimum(minimum)
    labelSize = histlist[0].GetXaxis().GetLabelSize()
    NbinsX = histlist[0].GetXaxis().GetNbins()
    histlist[0].GetXaxis().SetLabelSize(min(1.0/NbinsX,labelSize))
    if title != None: histlist[0].SetTitle(title)
    pads[0].cd()
    histlist[0].Draw("E")
    for h in histlist[1:]:
        h.Draw("sameE")
    pads[1].cd()
    legend.Draw()
    pads[0].SetLogy(log)
    if save != None: canvas.SaveAs(save)

def Stack(listOfHists,tags,title=None,save=None,log=False,minimum=0,suppressWarning=False):
    canvas.cd()
    histlist = [h.Clone(h.GetName()+"tmp") for h in listOfHists]
    if tags != None:
        if len(tags) < len(histlist): raise Exception("Not enough tags provided, {0} < {1}".format(len(tags),len(histlist)))
        else:
            if not suppressWarning and len(tags) > len(histlist): print "[NiftyHists] Warning: More tags provided than histograms. {0}, {1}".format(len(tags),len(histlist))
            histdict = dict(zip(histlist,tags))
    else:
        histdict = dict(zip(histlist,[h.GetTitle() for h in histlist]))
    legend.Clear()
    for h in histlist:
        legend.AddEntry(h,histdict[h])
    stack = ROOT.THStack()
    for h in histlist: stack.Add(h)
    if log and minimum == 0: minimum = 0.001
    stack.SetMinimum(minimum)
    if title != None: stack.SetTitle(title)
    pads[0].cd()
    stack.Draw("hist")
    pads[1].cd()
    legend.Draw()
    pads[0].SetLogy(log)
    if save != None: canvas.SaveAs(save)

def SimplePlot(hist,save=None,log=False,minimum=0,suppressWarning=False):
    simplecanvas.cd()
    simplecanvas.SetLogy(log)
    hist.SetMaximum(1.2*hist.GetMaximum())
    if log and minimum == 0: minimum = 0.001
    hist.SetMinimum(minimum)
    labelSize = hist.GetXaxis().GetLabelSize()
    NbinsX = hist.GetXaxis().GetNbins()
    hist.GetXaxis().SetLabelSize(min(1.0/NbinsX,labelSize))
    hist.GetYaxis().SetTitleOffset(1.6)
    hist.Draw("E")
    if save != None: simplecanvas.SaveAs(save)
