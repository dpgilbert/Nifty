import ROOT

def HistComp (h):
    return h.Integral()

def OverlayScaledToMax(listOfHists,legend,tags,minimum=0,suppressWarning=False):
    histlist = [h.Clone(h.GetName()+"tmp") for h in listOfHists]
    if tags != None:
        if len(tags) < len(histlist): raise Exception("Not enough tags provided")
        elif not suppressWarning and len(tags) > len(histlist): print "[NiftyHists] Warning: More tags provided than histograms."
        else: histdict = dict(zip(histlist,tags))
    else:
        histdict = dict(zip(histlist,[h.GetTitle() for h in histlist]))
    sortedHists = sorted(histlist,key = HistComp,reverse=True)
    sortedHists[0].SetMinimum(minimum)
    sortedHists[0].Draw()
    if legend != None:
        legend.AddEntry(sortedHists[0],histdict[sortedHists[0]])
    for h in sortedHists[1:]:
        if (h.Integral() > 0):
            rescale = int(sortedHists[0].Integral() / h.Integral() )
        else:
            rescale = 1
        h.Scale(rescale)
        if legend != None:
            if rescale > 1:
                legend.AddEntry(h,histdict[h] + " x " + str(rescale))
            else: 
                legend.AddEntry(h,histdict[h])
        h.Draw("same")
    return

def OverlayScaledToMin(listOfHists,legend,tags,minimum=0,suppressWarning=False):
    histlist = [h.Clone(h.GetName()+"tmp") for h in listOfHists]
    if tags != None:
        if len(tags) < len(histlist): raise Exception("Not enough tags provided")
        elif not suppressWarning and len(tags) > len(histlist): print "[NiftyHists] Warning: More tags provided than histograms."
        else: histdict = dict(zip(histlist,tags))
    else:
        histdict = dict(zip(histlist,[h.GetTitle() for h in histlist]))
    sortedHists = sorted(histlist,key = HistComp,reverse=False)
    sortedHists[0].SetMinimum(minimum)
    sortedHists[0].Draw()
    if legend != None:
        legend.AddEntry(sortedHists[0],histdict[sortedHists[0]])
    for h in sortedHists[1:]:
        if (h.Integral() > 0):
            rescale = int(h_integral() / sortedHists[0].Integral())            
        else:
            rescale = 1
        h.Scale(1.0 / rescale)
        if legend != None:
            if rescale > 1:
                legend.AddEntry(h,histdict[h] + " x 1/" + str(rescale))
            else: 
                legend.AddEntry(h,histdict[h])
        h.Draw("same")
    return

def OverlayUnitArea(listOfHists,legend,tags,minimum=0,suppressWarning=False):
    histlist = [h.Clone(h.GetName()+"tmp") for h in listOfHists]
    if tags != None:
        if len(tags) < len(histlist): raise Exception("Not enough tags provided")
        elif not suppressWarning and len(tags) > len(histlist): print "[NiftyHists] Warning: More tags provided than histograms."
        else: histdict = dict(zip(histlist,tags))
    else:
        histdict = dict(zip(histlist,[h.GetTitle() for h in histlist]))
    for h in histlist:
        integral = int(h.Integral())
        if integral > 0:
            h.Scale(1.0 / integral)
        if legend != None:
            legend.AddEntry(h,histdict[h] + " (" + str(integral) + ")")
    histlist[0].SetMaximum(1.2 * max([h.GetMaximum() for h in histlist]))
    histlist[0].SetMinimum(minimum)
    histlist[0].Draw()
    for h in histlist[1:]:
        h.Draw("same")
    return

def Overlay(listOfHists,legend,tags,minimum=0,suppressWarning=False):
    histlist = [h.Clone(h.GetName()+"tmp") for h in listOfHists]
    if tags != None:
        if len(tags) < len(histlist): raise Exception("Not enough tags provided")
        elif not suppressWarning and len(tags) > len(histlist): print "[NiftyHists] Warning: More tags provided than histograms."
        else: histdict = dict(zip(histlist,tags))
    else:
        histdict = dict(zip(histlist,[h.GetTitle() for h in histlist]))
    for h in histlist:
        if legend != None:
            legend.AddEntry(h,histdict[h])
    histlist[0].SetMaximum(1.2 * max([h.GetMaximum() for h in histlist]))
    histlist[0].SetMinimum(minimum)
    histlist[0].Draw()
    for h in histlist[1:]:
        h.Draw("same")
    return


