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

#Single Gamma
#"SingleGammaPt25Eta1p6_2p8/crab_SingleGammaPt25_PU0-threshold/181031_145212/0000"
#"SingleGammaPt25Eta1p6_2p8/crab_SingleGammaPt25_PU0-stc/181031_145114/0000"
#VBF
#"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_threshold/181108_112741/0000"
#"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_stc/181108_104142/0000"
#"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_threshold-histoMax/181113_145731/0000"
#"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_stc-histoMax/181113_145456/0000"

queue = "8nh" # give bsub queue -- 8nm (8 minutes), 1nh (1 hour), 8nh, 1nd (1day), 2nd, 1nw (1 week), 2nw 
########   customization end   #########

InputDirList = [ 
#   "SingleGammaPt25Eta1p6_2p8/crab_SingleGamma-PU0-threshold-TCs-histoMax-DR03/181121_113118/0000",
#   "SingleGammaPt25Eta1p6_2p8/crab_SingleGamma-PU0-stc-TCs-histoMax-DR03/181121_113207/0000",
#   "SingleGammaPt25Eta1p6_2p8/crab_SingleGamma-PU200-threshold-TCs-histoMax-DR03/181121_115525/0000",
#   "SingleGammaPt25Eta1p6_2p8/crab_SingleGamma-PU200-stc-TCs-histoMax-DR03/181121_115450/0000"

# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-threshold0p5-default-3sigSensorThreshold/190411_094137/0000",
# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-threshold1p0-default-3sigSensorThreshold/190411_101248/0000",
# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-threshold1p5-default-3sigSensorThreshold/190411_101334/0000",


# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-threshold0-default-2sigSensorThreshold/190411_100202/0000",
# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-threshold0-default-4sigSensorThreshold/190411_100020/0000",
# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-threshold0-default-5sigSensorThreshold/190411_095923/0000",

# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-STC2_SimpleCoarsening-default-NewSensorThreshold-Fix-2/190412_115121/0000",
# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-STC4-default-2sigSensorThreshold/190412_115657/0000",
# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-STC4-default-3sigSensorThreshold/190412_115912/0000",
# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-STC4-default-4sigSensorThreshold/190412_120258/0000",
# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-STC4-default-5sigSensorThreshold/190412_120509/0000",

# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-ThickCoarse-1bit-default/190415_162613/0000",
# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-ThickCoarse-STC4-default/190415_162400/0000",
# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-ThickCoarse-EqualShare-default/190415_162516/0000",

# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-ThickCoarse-1bit-default/190416_101946/0000",
# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-ThickCoarse-STC4-default/190416_101729/0000",
# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-ThickCoarse-EqualShare-default/190416_101837/0000",


# "/SinglePion_FlatPt-2to100/crab_SinglePionFlatPt-PU200-Threshold/190416_151852/0000/",
# "/SinglePion_FlatPt-2to100/crab_SinglePionFlatPt-PU200-STC4/190416_151809/0000/",

"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU0-ThickCoarse-1bit-default/190425_124354/0000",
# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU0-ThickCoarse-STC4-default/190417_153733/0000",
# "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU0-ThickCoarse-EqualShare-default/190417_154700/0000",


"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-ThickCoarse-STC4-Radx1p5/190425_124449/0000",
"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-ThickCoarse-EqualShare-Radx1p5/190425_124529/0000",
"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_VBF-PU200-ThickCoarse-1bit-Radx1p5/190425_124607/0000",

]

#TreeNames = [ "Floatingpoint8ThresholdRef2dRef3dGenclustersntuple", "Floatingpoint8SupertriggercellDummyHistomaxClustersntuple" ]

TreeNames = [ "hgcalTriggerNtuplizer" ]


OutputDirList = [

   "VBF-PU0-ThickCoarse-1bit-default",

   "VBF-PU200-ThickCoarse-STC4-Radx1p5",
   "VBF-PU200-ThickCoarse-EqualShare-Radx1p5",
   "VBF-PU200-ThickCoarse-1bit-Radx1p5",
  # "VBF-PU0-ThickCoarse-STC4-default",
  # "VBF-PU0-ThickCoarse-EqualShare-default",

   # "SinglePionFlatPt-PU200-Threshold",
   # "SinglePionFlatPt-PU200-STC4",

  # "VBF-PU200-ThickCoarse-1bit-default",
  # "VBF-PU200-ThickCoarse-STC4-default",
  # "VBF-PU200-ThickCoarse-EqualShare-default",
   
 # "VBF-PU200-STC2_SimpleCoarsening-default-NewSensorThreshold-Fix-2",
 # "VBF-PU200-STC4-default-2sigSensorThreshold",
 # "VBF-PU200-STC4-default-4sigSensorThreshold",
 # "VBF-PU200-STC4-default-3sigSensorThreshold",
 # "VBF-PU200-STC4-default-5sigSensorThreshold",

 # "VBF-PU200-threshold0p5-default-3sigSensorThreshold",
 # "VBF-PU200-threshold1p0-default-3sigSensorThreshold",
 # "VBF-PU200-threshold1p5-default-3sigSensorThreshold",
 # "VBF-PU200-threshold0-default-2sigSensorThreshold",
 # "VBF-PU200-threshold0-default-4sigSensorThreshold",
 # "VBF-PU200-threshold0-default-5sigSensorThreshold",



   ]

path = os.getcwd()

if subprocess.call(["voms-proxy-info",'--exists']) == 1:
   print "Voms proxy does not exist:"
   os.system("voms-proxy-init -voms cms -valid 96:00")
else:
   print "Voms proxy exists"
print

##### loop for creating and sending jobs #####
for indir, outdir in zip( InputDirList, OutputDirList ):

   print
   print 'do not worry about folder creation:'
   print "res/" + outdir
   os.system("rm -r tmp/" + outdir)
   os.system("rm -r res/" + outdir)
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
         fout.write("python "+ScriptName+" --input='root://cms-xrd-global.cern.ch//store/user/sawebb/" + indir + "/ntuple_'\"$FILENAME\"'.root' -p 'input:tree:\"" + treename + "\"' --output='res/"+outdir + "/" + OutputFileNames+"_'\"$FILENAME\"'.root'\n")
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
         fout.write("queue " + str(NumberOfJobs))
         
   ###### sends condor jobs ######
      os.system("condor_submit condor.sub")
      
   


   os.chdir("../../")
   

   
print
print "your jobs:"
os.system("condor_q")
print
print 'END'
print
