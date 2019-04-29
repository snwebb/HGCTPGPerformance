from array import array
import numpy as np

class parameters :
    def __init__(self):
        self.calibration={"do":False,#Default false
                "type":"inversion","constants":[
                1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 
                ],
                "cut":[ ## raw, 0 below the cut
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                ],
                #"pt-eta":"",
                "pt-eta":"4.4374 -0.948102 *TMath::Log(TMath::Max(x,20.)) + 0.0686934* TMath::Log(TMath::Max(x,20.)) * TMath::Log(TMath::Max(x,20.))", ## nopu
                #"pt-eta":"0.577536*TMath::Erfc(-1.11941*x+4.30494)",                ## pu200
                }
        
        self.matrix_calibration={"file":"matrix_calibration.root"}

        ## cluster parameters
        self.cluster = {"dR": float(0.4), "ptmin":float(0.5)}
        self.cluster_input = {"cl3D"}
#        self.cluster_input = {"tc"}
        ## tree name
        self.output = {"tree":"jets","file":"output.root"}
        self.input = {"tree":"hgcalTriggerNtuplizer"}

        ## to run, only needed if gen_jets is running
        #        self.torun=['efficiency_pteta','fake_pteta','resolution_pt','turn_on']
        self.torun=[]
        ## 

        self.dr_jet = 0.2
        self.efficiency = {"ptbins":array('d',[20,30,40,50]),"etabins":array('d',[1.7,2.0,2.2,2.5,2.7]),"abseta":True,"dR":float(0.3)}
        self.fake = {"ptbins":array('d',[20,30,40,50]),"etabins":array('d',[1.7,2.0,2.2,2.5,2.7]),"abseta":True,"dR":float(0.3)}
        self.resolution = {"bins":np.arange(-2.0,10, .1,dtype='d'),"dR":float(0.3),"ptbins":array('d',[30.,40,50,60,70,80,90,100,120,150,200,300,500,1000,2000,3000])}
        self.turnon = {"ptbins":array('d',range(30,1000)),"dR":float(0.3),"ptcut":[float(50),float(100),float(150),float(200.)]}
        self.layer_deposits= {'ptcut':[30,40,50,80,100,200,500,1000],
                'dR':0.4
                }  
