import ROOT

def GetKeyNames( self, dir = "" ):
        self.cd(dir)
        return [dir+"/"+key.GetName() for key in ROOT.gDirectory.GetListOfKeys() if not key.IsFolder()]
ROOT.TFile.GetKeyNames = GetKeyNames

