import ROOT
import graphviz as gv
import sys

ROOT.gROOT.SetBatch(True)

if len(sys.argv) < 4:
    print "Need a cms4 file, an output tag, and at least 1 event index"
    exit(1)

cms4_filename = sys.argv[1]
outtag = sys.argv[2]
events = sys.argv[3:]

cms4_file = ROOT.TFile.Open(cms4_filename)
cms4_tree = cms4_file.Get("Events")

pdgId_dict = {
1 : "u",
2 : "d",
3 : "s",
4 : "c",
5 : "b",
6 : "t",
11 : "e",
12 : "v_e",
13 : "mu",
14 : "v_mu",
15 : "tau",
16 : "v_tau",
21 : "glu",
22 : "pho",
23 : "Z",
24 : "W",
25 : "H",
111 : "pi0",
113 : "rho0",
130 : "K_L",
213 : "rho+/-",
211 : "pi+/-",
221 : "eta",
310 : "K_S",
311 : "K_0",
321 : "K+/-",
2212 : "p",
1000021 : "gluino",
1000022 : "LSP",
1000024 : "chargino"
}

def getName(pdgId):
    return pdgId_dict.get(abs(pdgId),str(abs(pdgId)))

def MakeTree(IDs, motherIDXs):
    t = gv.Digraph() # use format=".xyz" in constructor to change to desired format, defaults to pdf
    t.node("0","p")
    t.node("1","p")
    for i,ID in enumerate(IDs):
        if (i < 2): continue
        motherID = IDs[motherIDXs[i]]
        t.node(str(ID),getName(ID))
        t.edge(str(motherID),str(ID))
    return t
        
for event in events:
    cms4_tree.GetEntry(int(event))
    gvtree = MakeTree(cms4_tree.genps_id, cms4_tree.genps_idx_mother)
    gvtree.render("{0}_{1}".format(outtag,str(event)))

del cms4_tree
cms4_file.Close()
    

