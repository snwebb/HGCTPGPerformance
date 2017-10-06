## producer of jet out of clusters
## ntuples version
## Andrea Carlo Marini -- Thu Jun 29 15:30:22 CEST 2017

import ROOT
import hgc_tpg.utilities.functions as f
import numpy as np
from glob import glob
import sys
from datetime import datetime
import math

## using pyjet
from pyjet import cluster, DTYPE_EP, DTYPE_PTEPM

class calibration_inputs:
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
        self.dR=conf.match["dR"]
        self.xmin = conf.output["xmin"]
        self.xmax = conf.output["xmax"]
        self.nbins = conf.output["nbins"]
        self.histos = {}
        self.cfg = conf

        ## Collections of TLorentzVector
        self.time_=None


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
        
        nentries=self.chain.GetEntries()
        for ientry,entry in enumerate(self.chain):
            self.print_progress(ientry,nentries)

            #self.clear()
            #c3d_pt_ = np.array(entry.cl3d_pt)
            #c3d_eta_ = np.array(entry.cl3d_eta)
            #c3d_phi_ = np.array(entry.cl3d_phi)
            #c3d_energy_ = np.array(entry.cl3d_energy)

            gen_pt_ = np.array(entry.gen_pt)
            gen_eta_ = np.array(entry.gen_eta)
            gen_phi_ = np.array(entry.gen_phi)
            gen_energy_ = np.array(entry.gen_energy)
            gen_status_ = np.array(entry.gen_status)
            gen_id_ = np.array(entry.gen_id)

            cl_pt_ = np.array(entry.cl_pt)
            cl_eta_ = np.array(entry.cl_eta)
            cl_phi_ = np.array(entry.cl_phi)
            cl_energy_ = np.array(entry.cl_energy)
            cl_layer_ = np.array(entry.cl_layer)
            cl_ncells_ = np.array(entry.cl_ncells)
            ##FIXME ??? check
            cl_cells_ = np.array(entry.cl_cells) ### ?

            tc_data_ = np.array(entry.tc_data)

            for igen in range(0,len(gen_pt_)):
                if gen_status_[igen] != 1: continue
                if abs(gen_id_[igen]) != 11: continue ## electron

                for icl in range(0,len(cl_pt_)):
                    if f.deltaR( cl_eta_[icl], gen_eta_[igen],cl_phi_[icl],gen_phi_[igen])> self.dR : continue
                    ## MATCHED
                    # 1. compute raw energy in the c2d
                    raw= 0.0
                    for icell in range(0,cl_ncells_[icl]):
                        raw += tc_data_ [ cl_cells_[icl][icell]] 
                    # 2. save a histogram with the calibrated energy and the raw energy
                    # nominal and pt
                    name = "raw_layer_%d_truept_%.0f"%(cl_layer_[icl],gen_pt_[igen])
                    if name not in self.histos:
                        self.histos[name] = ROOT.TH1D(name,name,self.nbins,self.xmin,self.xmax)
                    self.histos[name].Fill(raw)

                    name = "rawt_layer_%d_truept_%.0f"%(cl_layer_[icl],gen_pt_[igen])
                    t= math.exp(-cl_eta_[icl]) ## tan theta/2
                    sint = 2*t/(1+t*t) ## sin theta
                    if name not in self.histos:
                        self.histos[name] = ROOT.TH1D(name,name,self.nbins,self.xmin,self.xmax)
                    self.histos[name].Fill(raw*sint)

                    name = "pt_layer_%d_truept_%.0f"%(cl_layer_[icl],gen_pt_[igen])
                    if name not in self.histos:
                        self.histos[name] = ROOT.TH1D(name,name,self.nbins,self.xmin,self.xmax)
                    self.histos[name].Fill(cl_pt_[icl])


            ## produce trigger jets and gen jets

        self.output.cd()
        for hStr  in self.histos:
            self.histos[hStr].Write()
        return self
