from array import array
import numpy as np

class parameters :
    def __init__(self):
        ##
        self.calibration={"do":False,
                "type":"inversion","constants":[
                #1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 
                #1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 
                1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 1.084, 
                ],
                "cut":[ ## raw, 0 below the cut
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                ],
                ## 
                #"pt-eta":"",
                "pt-eta":"4.4374 -0.948102 *TMath::Log(TMath::Max(x,20.)) + 0.0686934* TMath::Log(TMath::Max(x,20.)) * TMath::Log(TMath::Max(x,20.))", ## nopu
                # this are on the jets
                #"pt-eta2":"-21.235 + 22.8461*TMath::Log(TMath::Max(x,20.))  -9.03475 * TMath::Power(TMath::Max(x,20.),2) + 1.72068*TMath::Power(TMath::Max(x,20.),3) -0.158798*TMath::Power(TMath::Max(x,20.),4) + 0.00570914 * TMath::Power(TMath::Max(x,20.),5) ",


                ## pu200
                #"pt-eta":"0.577536*TMath::Erfc(-1.11941*x+4.30494)",

                }
        
        ## with X
        ##p0                        =       4.4374   +/-   0.163509    
        ##p1                        =    -0.948102   +/-   0.0636644   
        ##p2                        =    0.0686934   +/-   0.00599335  
        ## second round
        ## p0                        =      -21.235   +/-   17.0892     
        ## p1                        =      22.8461   +/-   17.0915     
        ## p2                        =     -9.03475   +/-   6.74443     
        ## p3                        =      1.72068   +/-   1.31273     
        ## p4                        =    -0.158798   +/-   0.126052    
        ## p5                        =   0.00570914   +/-   0.00477836  
        ## PU 200
        ## p0                        =     0.577536   +/-   0.010146    
        ## p1                        =     -1.11941   +/-   0.111525    
        ## p2                        =      4.30494   +/-   0.4418   

        ##
        self.matrix_calibration={"file":"matrix_calibration.root"}

        ## cluster parameters
        self.cluster = {"dR": float(0.4), "ptmin":float(0.5)}
        self.cluster_input = {"cl3D"}
#        self.cluster_input = {"tc"}
        ## tree name
        self.output = {"tree":"jets","file":"output.root"}

        ## to run
        self.torun=['efficiency_pteta','fake_pteta','resolution_pt','turn_on']
        #self.torun=['matrix_calibration'] ## set also calib to false
        ## 

        self.dr_jet = 0.2
        self.efficiency = {"ptbins":array('d',[20,30,40,50]),"etabins":array('d',[1.7,2.0,2.2,2.5,2.7]),"abseta":True,"dR":float(0.3)}
        self.fake = {"ptbins":array('d',[20,30,40,50]),"etabins":array('d',[1.7,2.0,2.2,2.5,2.7]),"abseta":True,"dR":float(0.3)}
        #self.resolution = {"bins":np.arange(-10.0,10.0, 0.01,dtype='d'),"dR":float(0.3),"ptbins":array('d',[30.,40,50,60,70,80,90,100,120,150,200,300,500,1000,2000,3000])}
        self.resolution = {"bins":np.arange(-2.0,10, .1,dtype='d'),"dR":float(0.3),"ptbins":array('d',[30.,40,50,60,70,80,90,100,120,150,200,300,500,1000,2000,3000])}
        #self.turnon = {"ptbins":array('d',range(30,1000)),"dR":float(0.3),"ptcut":[float(35.),float(80.),float(120),float(500.)]}
        self.turnon = {"ptbins":array('d',range(30,1000)),"dR":float(0.3),"ptcut":[float(50),float(100),float(150),float(200.)]}
        self.layer_deposits= {'ptcut':[30,40,50,80,100,200,500,1000],
                'dR':0.4
                }  
