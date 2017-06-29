from array import array

class parameters :
    def __init__(self):
        ## cluster parameters
        self.cluster = {"dR": float(0.4), "ptmin":float(3.0)}

        ## tree name
        self.output = {"tree":"jets","file":"output.root"}

        ## 
        self.efficiency = {"ptbins":array('d',[20,30,40,50]),"etabins":array('d',[1.7,2.0,2.2,2.5,2.7]),"abseta":True,"dR":float(0.3)}
