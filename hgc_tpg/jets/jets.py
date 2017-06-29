## producer of jet out of clusters
## ntuples version
## Andrea Carlo Marini -- Thu Jun 29 15:30:22 CEST 2017

import ROOT
import hgc_tpg.utilities.functions as f
import numpy as np

## using pyjet
from pyjet import cluster, DTYPE_EP, DTYPE_PTEPM


class jet_clustering:
    ''' Jet Clustering '''
    def __init__(self, input_file, conf):
        self.inputNtuple=ROOT.TFile.Open(input_file)
        self.chain = self.inputNtuple.Get("hgcalTriggerNtuplizer/HGCalTriggerNtuple")

        self.output = ROOT.TFile(conf.output['file'],"RECREATE")
        self.tree_out = ROOT.TTree(conf.output ['tree'],conf.output['tree'])
        self.cfg = conf

        ## Collections of TLorentzVector
        self.jets_ = []
        self.genjets_ = []

    def clear(self):
        self.jets_=[]
        self.genjets_=[]

    def do_clusters(self,ptV,etaV,phiV,energyV ):
        ''' run the clustering on the input std vectors'''
        n=len(ptV)
        if len(etaV) != n : raise ValueError('input vectors have different length')
        if len(phiV) != n : raise ValueError('input vectors have different length')
        if len(energyV) != n : raise ValueError('input vectors have different length')
        
        input_particles = []
        for i in range(0,n):
            p = ROOT.TLorentzVector()
            p.SetPtEtaPhiE(ptV[i],etaV[i],phiV[i],energyV[i])
            input_particles.append( (p.Pt(),p.Eta(),p.Phi(),p.M())  )
       
        ip = np.array( input_particles, dtype=DTYPE_PTEPM)
        sequence=cluster( ip, algo="antikt",ep=False,R=0.4)
        jets = sequence.inclusive_jets()

        for i, jet in enumerate(jets):
            #print("{0: <5} {1: 10.3f} {2: 10.3f} {3: 10.3f} {4: 10.3f} {5: 10}".format(
            #    i + 1, jet.pt, jet.eta, jet.phi, jet.mass, len(jet)))
            p = ROOT.TLorentzVector()
            p.SetPtEtaPhiM(  jet.pt, jet.eta, jet.phi, jet.mass)
            self.jets_ .append(p) 
        return self

    def do_genjets(self,ptV,etaV,phiV,energyV):
        ''' just grab genjets and put in the class collection'''
        for pt, eta, phi, energy in zip( ptV,etaV,phiV,energyV):
            p = ROOT.TLorentzVector()
            p.SetPtEtaPhiE(  pt, eta, phi, energy)
            self.genjets_ .append(p) 
        return self
   
    class efficiency_pteta:
        def __init__(self,outer):
            self.outer=outer

            ptbins=outer.cfg.efficiency['ptbins']
            etabins=outer.cfg.efficiency['etabins']
            self.eff_num = ROOT.TH2D("num","eff. num",len(ptbins)-1,ptbins,len(etabins)-1,etabins)
            self.eff_den = ROOT.TH2D("den","eff. den",len(ptbins)-1,ptbins,len(etabins)-1,etabins)
            self.useAbsEta = outer.cfg.efficiency["abseta"]
            self.dR= outer.cfg.efficiency["dR"]

        def run(self):
            for igen, gj in enumerate(self.outer.genjets_):
                match=False
                for itr, jet in enumerate(self.outer.jets_):
                    if gj.DeltaR(jet) < self.dR: 
                        match = True
                        break
                eta = gj.Eta()
                pt = gj.Pt()
                if self.useAbsEta: eta = abs(eta)
                self.eff_den.Fill(pt,eta)
                if match:  self.eff_num.Fill(pt,eta)
            return self

        def finalize(self):        
            self.eff_h = self.eff_num.Clone("eff")
            self.eff_h.Divide(self.eff_den)
            for h in [ self.eff_h,self.eff_num,self.eff_den] :
                h.Write()
            return self


    def loop(self):
        todo=[self.efficiency_pteta(self) ] 

        for ientry,entry in enumerate(self.chain):
            self.clear()
            c3d_pt_ = np.array(entry.cl3d_pt)
            c3d_eta_ = np.array(entry.cl3d_eta)
            c3d_phi_ = np.array(entry.cl3d_phi)
            c3d_energy_ = np.array(entry.cl3d_energy)

            genjets_pt_ = np.array(entry.genjet_pt)
            genjets_eta_ = np.array(entry.genjet_eta)
            genjets_phi_ = np.array(entry.genjet_phi)
            genjets_energy_ = np.array(entry.genjet_energy)

            ## produce trigger jets and gen jets
            self.do_clusters(c3d_pt_,c3d_eta_,c3d_phi_,c3d_energy_).do_genjets( genjets_pt_,genjets_eta_,genjets_phi_,genjets_energy_)

            ## produce plots
            for x in todo: x.run()
        self.output.cd()
        for x in todo: x.finalize()
        return self
