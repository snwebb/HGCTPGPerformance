from array import array
import numpy as np

class parameters :
    def __init__(self):
        ## cluster parameters
        self.cluster = {"dR": float(0.4), "ptmin":float(3.0)}

        ## tree name
        self.output = {"tree":"jets","file":"output.root"}

        ## to run
        self.torun=['efficiency_pteta','fake_pteta','resolution_pt','turn_on']
        ## 
        self.efficiency = {"ptbins":array('d',[20,30,40,50]),"etabins":array('d',[1.7,2.0,2.2,2.5,2.7]),"abseta":True,"dR":float(0.3)}
        self.fake = {"ptbins":array('d',[20,30,40,50]),"etabins":array('d',[1.7,2.0,2.2,2.5,2.7]),"abseta":True,"dR":float(0.3)}
        self.resolution = {"bins":np.arange(-1.2,1.2, 0.01,dtype='d'),"dR":float(0.3),"ptbins":array('d',[30.,40,50,60,70,80,90,100,120,150,200,300,500,1000,2000,3000])}
        self.turnon = {"ptbins":array('d',range(30,1000)),"dR":float(0.3),"ptcut":[float(35.),float(80.),float(120),float(500.)]}
