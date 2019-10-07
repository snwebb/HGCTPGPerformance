#!/usr/bin/env python
import os, re, subprocess
import commands
import math, time
import sys

print 
print 'START'
print 
########   YOU ONLY NEED TO FILL THE AREA BELOW   #########
########   customization  area #########
NumberOfJobs= 100 # number of jobs to be submitted
#NumberOfJobs= 1 # number of jobs to be submitted
interval = 1 # number files to be processed in a single job, take care to split your file so that you run on all files. The last job might be with smaller number of files (the ones that remain).
OutputFileNames = "ntuple_jet" # base of the output file name, they will be saved in res directory
#OutputFileNames = "ntuple_res" # base of the output file name, they will be saved in res directory
ScriptName = "scripts/runJets.py" # script to be used with cmsRun
#ScriptName = "scripts/runResolution.py" # script to be used with cmsRun

queue = "8nh" # give bsub queue -- 8nm (8 minutes), 1nh (1 hour), 8nh, 1nd (1day), 2nd, 1nw (1 week), 2nw 
########   customization end   #########

InputDirList = [ 

#V9 (EXTENDED CLUSTER RADIUS)
# "VBFHToTauTau_M125_14TeV_powheg_pythia8/crab_VBF-HTT-PU200-MultiAlgo-Threshold-DR1p75/190610_160411/0000",
# "VBFHToTauTau_M125_14TeV_powheg_pythia8/crab_VBF-HTT-PU200-MultiAlgo-SuperTCs-DR1p75/190610_160541/0000",
# "VBFHToTauTau_M125_14TeV_powheg_pythia8/crab_VBF-HTT-PU200-MultiAlgo-SeedThreshold-DR1p75/190610_161108/0000",


#V8 (EXTENDED CLUSTER RADIUS)
#"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-MultiAlgo-Threshold-DR1p75/190610_161427/0000",
#"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-MultiAlgo-SuperTCs-DR1p75/190610_161652/0000",
#"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-MultiAlgo-SeedThreshold-DR1p75/190610_161347/0000",



#V9 HGG (DEFAULT CLUSTER RADIUS)
#"VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-MultiAlgo-Threshold/190612_085552/0000",
#"VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-MultiAlgo-SuperTCs/190611_103109/0000",




#"VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-MultiAlgo-Threshold-WS/190614_103104/0000",
#"VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-MultiAlgo-SuperTCs-WS/190614_103316/0000",
# "VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-MultiAlgo-SeedThreshold-WS/190614_103718/0000",
# "VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-MultiAlgo-ClusterRadius-WS/190614_103923/0000",

#"VBFHToTauTau_M125_14TeV_powheg_pythia8/crab_VBF-HTT-PU200-MultiAlgo-Threshold-WS/190614_103007/0000",
#"VBFHToTauTau_M125_14TeV_powheg_pythia8/crab_VBF-HTT-PU200-MultiAlgo-SuperTCs-WS/190614_103237/0000",
# "VBFHToTauTau_M125_14TeV_powheg_pythia8/crab_VBF-HTT-PU200-MultiAlgo-SeedThreshold-WS/190614_103645/0000",
# "VBFHToTauTau_M125_14TeV_powheg_pythia8/crab_VBF-HTT-PU200-MultiAlgo-ClusterRadius-WS/190614_103833/0000",

#"VBFHToTauTau_M125_14TeV_powheg_pythia8/crab_VBF-HTT-PU200-Default-WithTriggerCells-WS/190614_132424/0000",


#"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-MultiAlgo-Threshold-WS/190617_142337/0000",
#"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-MultiAlgo-SuperTCs-WS/190617_155355/0000",
#"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-MultiAlgo-SeedThreshold-WS/190617_155622/0000",
#"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-MultiAlgo-ClusterRadius-WS/190617_/0000",





# "VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-MultiAlgo-Decentralised/190709_130200/0000",
# "NeutrinoGun_E_10GeV/crab_DoubleNu-PU200-MultiAlgo-Decentralised/190709_130228/0000",
# "VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-MultiAlgo-Decentralised/190717_141103/0000",
# "NeutrinoGun_E_10GeV/crab_DoubleNu-PU200-MultiAlgo-Decentralised/190717_141958/0000",

# "VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-MultiAlgo-Decentralised-BugFix/190718_161801/0000",
# "NeutrinoGun_E_10GeV/crab_DoubleNu-PU200-MultiAlgo-Decentralised-BugFix/190718_161654/0000",

#"VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-Default/190726_142831/0000",



# "VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-Decentralised/190730_112632/0000",
# "NeutrinoGun_E_10GeV/crab_DoubleNu-PU200-Decentralised/190731_092913/0000",

# "RelValDiQ_Pt20To300_Etam1p6Tom2p9/crab_QuarkGun-Neg-PU0-Decentralised/190802_100839/0000",
# "RelValDiQ_Pt20To300_Etam1p6Tom2p9/crab_QuarkGun-Neg-PU140-Decentralised/190802_100807/0000",
# "RelValDiQ_Pt20To300_Etam1p6Tom2p9/crab_QuarkGun-Neg-PU200-Decentralised/190802_100732/0000",

# "RelValDiQ_Pt20To300_Eta1p6To2p9/crab_QuarkGun-Pos-PU0-Decentralised/190802_100704/0000",
# "RelValDiQ_Pt20To300_Eta1p6To2p9/crab_QuarkGun-Pos-PU140-Decentralised/190802_100633/0000",
# "RelValDiQ_Pt20To300_Eta1p6To2p9/crab_QuarkGun-Pos-PU200-Decentralised/190802_100555/0000",

#"VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-Decentralised-SignalDriven/190822_123250/0000",
#"VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-Default-withTCs/190822_132142/0000",


#"NeutrinoGun_E_10GeV/crab_DoubleNu-PU200-Decentralised-SignalDriven/190905_140242/0000",

#"VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-Default-withTCs-LayerInfo/190913_134251/0000",

#"NeutrinoGun_E_10GeV/crab_DoubleNu-PU200-Default-withTCs/190916_134011/0000",


# "RelValDiQ_Pt20To300_Eta1p6To2p9/crab_QuarkGun-Pos-PU0-Decentralised/190926_093004/0000",
# "RelValDiQ_Pt20To300_Eta1p6To2p9/crab_QuarkGun-Pos-PU140-Decentralised/190926_093906/0000",
# "RelValDiQ_Pt20To300_Eta1p6To2p9/crab_QuarkGun-Pos-PU200-Decentralised/190926_093951/0000",

#"VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-MixedFE-EM/190927_143347/0000",

#"VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-BestChoice-Coarser/191002_102809/0000",

#"VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU0-BestChoice-CoarserInH-Fix/191003_164218/0000",

"VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-SuperTC-Old/191004_084722/0000",
"VBFHToGG_M-125_14TeV_powheg_pythia8/crab_VBF-HGG-PU200-SuperTC-Validation/191004_083722/0000",

]


TreeNames = [

#SEED THRESHOLD

#  "Fp8ThresholdDummyHistomaxvardrth0Ntup",
#  "Fp8ThresholdDummyHistomaxvardrth10Ntup",
#  "Fp8ThresholdDummyHistomaxvardrth20Ntup",
#  "Fp8ThresholdDummyHistomaxvardrth40Ntup",

# "Fp8ThresholdDummyHistomaxNtup",
# "Fp8Stc4161616DummyHistomaxbin4Ntup",
# "Fp8BestchoiceDummyHistomaxNtup",


#DRHO

# "Fp8ThresholdDummyHistomaxvardrdrho1p0Ntup",
# "Fp8ThresholdDummyHistomaxvardrdrho1p5Ntup",
# "Fp8ThresholdDummyHistomaxvardrdrho2p0Ntup",
# "Fp8ThresholdDummyHistomaxvardrdrho5p0Ntup",




# "Fp8ThresholdDummyHistomaxNtup",
"Fp8Stc4444FixedDummyHistomaxNtup",
# "Fp8BestchoiceDummyHistomaxNtup",




# "Fp8ThresholdDummyHistomaxNtup",
   "Fp8Stc4161616DummyHistomaxNtup",
# "Fp8BestchoiceDummyHistomaxNtup",
# "Fp8MixedDummyHistomaxNtup",


# "Fp8BestchoiceDummyHistomaxNtup",
# "Fp8BestchoiceCoarse1DummyHistomaxNtup",
# "Fp8BestchoiceCoarse2DummyHistomaxNtup",
# "Fp8BestchoiceCoarse4DummyHistomaxNtup",
# "Fp8BestchoiceCoarse8DummyHistomaxNtup",
# "Fp8BestchoiceCoarse16DummyHistomaxNtup",

#default

#"hgcalTriggerNtuplizer",

 ]


#TreeNames = [ "Floatingpoint8ThresholdRef2dRef3dGenclustersntuple", "Floatingpoint8SupertriggercellDummyHistomaxClustersntuple" ]

#TreeNames = [ "hgcalTriggerNtuplizer" ]


Tag = "-DR0p2"
#Tag = ""

OutputDirList1=[  i.split("/")[1] for i in InputDirList ]
OutputDirList=[  i.split("_")[1] for i in OutputDirList1 ]


path = os.getcwd()

if subprocess.call(["voms-proxy-info",'--exists']) == 1:
   print "Voms proxy does not exist:"
   os.system("voms-proxy-init -voms cms -valid 96:00")
else:
   print "Voms proxy exists"
print

##### loop for creating and sending jobs #####
for indir, outdir in zip( InputDirList, OutputDirList ):

   outdir = outdir + Tag

   print
   print 'do not worry about folder creation:'
   print "res/" + outdir
   os.system("rm -r tmp/" + outdir)
#   os.system("rm -r res/" + outdir)
   os.system("mkdir -p tmp/" + outdir)
   os.system("mkdir -p res/" + outdir)
   print

   os.chdir("tmp/"+ outdir)

   #Loop over tree in file
   for treename in TreeNames:
      
      ##### creates jobs #######
      with open('job_' + treename + '.sh', 'w') as fout:
         fout.write("#!/bin/sh\n")
      
         fout.write("echo\n")
         fout.write("echo\n")
         fout.write("FILENAME=$(($2+1))\n")
         fout.write("echo 'START---------------'\n")
         fout.write("echo 'WORKDIR ' ${PWD}\n")
         fout.write("cd "+str(path)+"\n")
         fout.write("source /afs/cern.ch/work/s/sawebb/private/FastJet_HGC/HGCTPGPerformance/init_env_lxplus.sh\n")
         fout.write("export X509_USER_PROXY=/afs/cern.ch/user/s/sawebb/private/myVoms/x509up_u`id -u`\n")
         fout.write("python "+ScriptName+" --input='root://gfe02.grid.hep.ph.ic.ac.uk:1096//store/user/sawebb/" + indir + "/ntuple_'\"$FILENAME\"'.root' -p 'input:tree:\"" + treename + "\"'  -p 'output:tree:\"jets_" + treename + "\"' --output='res/"+outdir + "/" + OutputFileNames+"_" + treename + "_'\"$FILENAME\"'.root'\n")
#         fout.write("python "+ScriptName+" --input='ntuple.root' --output='res/"+outdir + "/" + OutputFileNames+"_'\"$FILENAME\"'.root' -p 'input:tree:\"Floatingpoint8ThresholdRef2dRef3dGenclustersntuple\"'\n")
         fout.write("echo 'STOP---------------'\n")
         fout.write("echo\n")
         fout.write("echo\n")
         os.system("chmod 755 job_" + treename + ".sh")
         
   ##### creates submit file #######
      with open('condor.sub', 'w') as fout:
         fout.write("executable            = job_"+treename+".sh \n")
         fout.write("arguments             = $(ClusterID) $(ProcId) \n")
         fout.write("output                = $(ClusterId).$(ProcId).out\n")
         fout.write("error                 = $(ClusterId).$(ProcId).err\n")
         fout.write("log                   = $(ClusterId).$(ProcId).log\n")
         fout.write("+JobFlavour           = \"workday\"\n") 
#         fout.write("+JobFlavour           = \"longlunch\"\n") 
#         fout.write("+JobFlavour           = \"microcentury\"\n") 
         fout.write("queue " + str(NumberOfJobs))
         
         ###### sends condor jobs ######
      os.system("condor_submit condor.sub")
      os.system("echo Waiting for 2 minutes")
#      os.system("sleep 180s")
      
   


   os.chdir("../../")
   

   
print
print "your jobs:"
os.system("condor_q")
print
print 'END'
print
