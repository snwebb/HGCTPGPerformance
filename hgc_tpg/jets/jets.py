## producer of jet out of clusters
## ntuples version
## Andrea Carlo Marini -- Thu Jun 29 15:30:22 CEST 2017

import ROOT
import hgc_tpg.utilities.functions as f
import numpy as np
from glob import glob
import sys
from datetime import datetime

## using pyjet
from pyjet import cluster, DTYPE_EP, DTYPE_PTEPM

class BaseRun:
    def __init__(self,outer):
        self.outer=outer

    def run(self):
        return self

    def finalize(self):
        return self

class efficiency_pteta(BaseRun):
    def __init__(self,outer):
        self.outer=outer

        ptbins=outer.cfg.efficiency['ptbins']
        etabins=outer.cfg.efficiency['etabins']
        self.eff_num = ROOT.TH2D("eff_num","eff. num",len(ptbins)-1,ptbins,len(etabins)-1,etabins)
        self.eff_den = ROOT.TH2D("eff_den","eff. den",len(ptbins)-1,ptbins,len(etabins)-1,etabins)
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

class fake_pteta(BaseRun):
    def __init__(self,outer):
        self.outer=outer

        ptbins=outer.cfg.fake['ptbins']
        etabins=outer.cfg.fake['etabins']
        self.fake_num = ROOT.TH2D("fake_num","fake. num",len(ptbins)-1,ptbins,len(etabins)-1,etabins)
        self.fake_den = ROOT.TH2D("fake_den","fake. den",len(ptbins)-1,ptbins,len(etabins)-1,etabins)
        self.useAbsEta = outer.cfg.fake["abseta"]
        self.dR= outer.cfg.fake["dR"]

    def run(self):
        for itr, jet in enumerate(self.outer.jets_):
            match=False
            for igen, gj in enumerate(self.outer.genjets_):
                if gj.DeltaR(jet) < self.dR: 
                    match = True
                    break
            eta = jet.Eta()
            pt = jet.Pt()
            if self.useAbsEta: eta = abs(eta)
            self.fake_den.Fill(pt,eta)
            if match:  self.fake_num.Fill(pt,eta)
        return self

    def finalize(self):        
        self.fake_h = self.fake_num.Clone("fake")
        self.fake_h.Divide(self.fake_den)
        for h in [ self.fake_h,self.fake_num,self.fake_den] :
            h.Write()
        return self

class resolution_pt(BaseRun):
    def __init__(self,outer):
        self.outer=outer

        bins=outer.cfg.resolution['bins']
        self.ptbins=outer.cfg.resolution['ptbins']
        self.res_h = {}
        for idx in range(0,len(self.ptbins)-1):
            self.res_h['pt%.0f_%.0f'%(self.ptbins[idx],self.ptbins[idx+1])]=ROOT.TH1D("res_pt%.0f_%.0f"%(self.ptbins[idx],self.ptbins[idx+1]),"res. pt %.0f %.0f"%(self.ptbins[idx],self.ptbins[idx+1]),len(bins)-1,bins)
        self.dR= outer.cfg.resolution["dR"]

    def run(self):
        for itr, jet in enumerate(self.outer.jets_):
            if jet.Pt()<20 : continue
            if abs(jet.Eta()) > 3.0 or abs(jet.Eta()) < 1.5 : continue
            match=False
            pt_gen=0
            for igen, gj in enumerate(self.outer.genjets_):
                if abs(gj.Eta()) > 3.0 or abs(gj.Eta()) < 1.5 : continue
                if gj.DeltaR(jet) < self.dR: 
                    match = True
                    pt_gen=gj.Pt()
                    break
            if match and pt_gen>5:  
                res = (jet.Pt() - pt_gen)/pt_gen
                for idx in range(0,len(self.ptbins)-1):
                    if pt_gen >= self.ptbins[idx] and pt_gen< self.ptbins[idx+1]:
                        self.res_h["pt%.0f_%.0f"%(self.ptbins[idx],self.ptbins[idx+1])].Fill(res)
        return self

    def finalize(self):        
        for h_str in self.res_h  :
            h=self.res_h[h_str]
            h.Write()
        return self

class turn_on(BaseRun):
    def __init__(self,outer):
        self.outer=outer

        self.ptcut=outer.cfg.turnon['ptcut']
        ptbins=outer.cfg.turnon['ptbins']
        self.dR= outer.cfg.turnon["dR"]
        
        self.turnon_num = {}
        self.turnon_den = {}
        for pt in self.ptcut:
            self.turnon_num["%.0f"%pt] = ROOT.TH1D("turnon_pt%.0f_num"%pt,"turnon.",len(ptbins)-1,ptbins)
            self.turnon_den["%.0f"%pt] = ROOT.TH1D("turnon_pt%.0f_den"%pt,"turnon.",len(ptbins)-1,ptbins)

    def run(self):
        for igen, gj in enumerate(self.outer.genjets_):
            match=False
            pt_reco=0.
            if abs(gj.Eta()) > 3.0 or abs(gj.Eta()) < 1.5 : continue
            for itr, jet in enumerate(self.outer.jets_):
                if abs(jet.Eta()) > 3.0 or abs(jet.Eta()) < 1.5 : continue
                if gj.DeltaR(jet) < self.dR: 
                    match = True
                    pt_reco=jet.Pt()
                    break
            if match:
                pt_gen=gj.Pt()
                for pt in self.ptcut:
                    self.turnon_den["%.0f"%pt].Fill(pt_gen)
                    if pt_reco> pt: self.turnon_num["%.0f"%pt].Fill(pt_gen)
        return self

    def finalize(self):        
        histos=[]
        for pt in self.ptcut:
            turnon_h = self.turnon_num["%.0f"%pt].Clone("turnon_pt%.0f"%pt)
            turnon_h.Divide(self.turnon_den["%.0f"%pt])
            histos.extend([turnon_h,self.turnon_num["%.0f"%pt],self.turnon_den["%.0f"%pt]])
        for h in histos :
            h.Write()
        return self


class jet_clustering:
    ''' Jet Clustering '''
    def __init__(self, input_file, conf):
        self.chain = ROOT.TChain("hgcalTriggerNtuplizer/HGCalTriggerNtuple")
        for template_name in input_file.split(','):
            if '*' in template_name:
                for f in glob(template_name):
                    self.chain.Add(f)
            else: ## regular files, xrootd, ...
                self.chain.Add(template_name)

        self.output = ROOT.TFile(conf.output['file'],"RECREATE")
        self.tree_out = ROOT.TTree(conf.output ['tree'],conf.output['tree'])
        self.cfg = conf

        ## Collections of TLorentzVector
        self.jets_ = []
        self.genjets_ = []
        self.time_=None

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
   

    def print_progress(self,done,tot,n=30,every=1000):
        if done % every != 0  and done < tot-1: return
        a=int(float(done)*n/tot )
        l="\r["
        if a==n: l += "="*n
        elif a> 0: l +=  "="*(a-1) + ">" + " "*(n-a)
        else: l += " "*n
        l+="] %.1f%%"%(float(done)*100./tot)
        if self.time_ == None: self.time_ = datetime.now()
        else: 
            new = datetime.now()
            delta=(new-self.time_)
            H=delta.seconds/3600 
            M=delta.seconds/60 -H*60
            S=delta.seconds - M*60-H*3600
            H+= delta.days*24
            if H>0:
                l+= " in %d:%d:%d s"%(H,M,S) 
            else:
                l+= " in %d:%d s"%(M,S) 
            S=int( (delta.seconds+24*3600*delta.days)*float(tot-done)/float(done) )
            M= S/60
            S-=M*60
            H= M/60
            M-=H*60
            l+= " will end in %d:%d:%d"%(H,M,S)
        if a==n: l+="\n"
        print l,
        sys.stdout.flush()
        return self

    def loop(self):
        #todo=[efficiency_pteta(self) ] 
        todo=[]
        print "-> Running on",
        for x in self.cfg.torun:
            print x,
            exec("todo.append("+x+"(self))")
        print 
        
        nentries=self.chain.GetEntries()
        for ientry,entry in enumerate(self.chain):
            self.print_progress(ientry,nentries)
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
