from array import array
import numpy as np

class parameters :
    def __init__(self):
        ## cluster parameters
        self.output={"file":"calibration.root",
                #"nbins":10000,"xmin":0,"xmax":100000
                "nbins":100000,"xmin":0,"xmax":1000000
                }
        self.match={"dR":0.4}
