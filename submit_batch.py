#!/usr/bin/env python
import os, re
import commands
import math, time
import sys

print 
print 'START'
print 
########   YOU ONLY NEED TO FILL THE AREA BELOW   #########
########   customization  area #########
NumberOfJobs= 100 # number of jobs to be submitted
interval = 1 # number files to be processed in a single job, take care to split your file so that you run on all files. The last job might be with smaller number of files (the ones that remain).
OutputFileNames = "ntuple_jet" # base of the output file name, they will be saved in res directory
#ScriptName = "scripts/runJets.py" # script to be used with cmsRun
ScriptName = "scripts/runResolution.py" # script to be used with cmsRun
#InputDir = "SingleGammaPt25Eta1p6_2p8/crab_SingleGammaPt25_PU0-threshold/181031_145212/0000"
InputDir = "SingleGammaPt25Eta1p6_2p8/crab_SingleGammaPt25_PU0-stc/181031_145114/0000"

#InputDir = "SinglePiPt100Eta1p6_2p8/crab_SinglePiPt100Eta1p6_2p8-threshold/181106_151745/0000"
#InputDir = "SinglePiPt100Eta1p6_2p8/crab_SinglePiPt100Eta1p6_2p8-stc/181106_112212/0000"
#FileList = "filelist.txt" # list with all the file directories
queue = "8nh" # give bsub queue -- 8nm (8 minutes), 1nh (1 hour), 8nh, 1nd (1day), 2nd, 1nw (1 week), 2nw 
########   customization end   #########

path = os.getcwd()
print
print 'do not worry about folder creation:'
os.system("rm -r tmp2")
os.system("rm -r res2")
os.system("mkdir tmp2")
os.system("mkdir res2")
print

##### loop for creating and sending jobs #####
for x in range(1, int(NumberOfJobs)+1):
   ##### creates directory and file list for job #######
   os.system("mkdir tmp2/"+str(x))
   os.chdir("tmp2/"+str(x))
   #os.system("sed '"+str(1+interval*(x-1))+","+str(interval*x)+"!d' ../../"+FileList+" > list.txt ")
   
   ##### creates jobs #######
   with open('job.sh', 'w') as fout:
      fout.write("#!/bin/sh\n")
      fout.write("echo\n")
      fout.write("echo\n")
      fout.write("echo 'START---------------'\n")
      fout.write("echo 'WORKDIR ' ${PWD}\n")
      fout.write("source /afs/cern.ch/work/s/sawebb/private/FastJet_HGC/HGCTPGPerformance/init_env_lxplus.sh\n")
      fout.write("export X509_USER_PROXY=/afs/cern.ch/user/s/sawebb/private/myVoms/x509up_u`id -u`\n")
      fout.write("cd "+str(path)+"\n")
      fout.write("python "+ScriptName+" --input='root://cms-xrd-global.cern.ch//store/user/sawebb/" + InputDir + "/ntuple_"+str(x)+".root' --output='res2/"+OutputFileNames+"_"+str(x)+".root'\n")
      fout.write("echo 'STOP---------------'\n")
      fout.write("echo\n")
      fout.write("echo\n")
   os.system("chmod 755 job.sh")


   ##### creates submit file #######
   with open('condor.sub', 'w') as fout:
      fout.write("executable            = job.sh \n")
      fout.write("arguments             = $(ClusterID) $(ProcId) \n")
      fout.write("output                = $(ClusterId).out\n")
      fout.write("error                 = $(ClusterId).err\n")
      fout.write("log                   = $(ClusterId).log\n")
      fout.write("+JobFlavour           = \"workday\"\n") 
      fout.write("queue")
   
   ###### sends bjobs ######
#   os.system("bsub -q "+queue+" -o logs job.sh")
   os.system("condor_submit condor.sub")
   print "job nr " + str(x) + " submitted"
   
   os.chdir("../..")
   
print
print "your jobs:"
os.system("condor_q")
print
print 'END'
print
