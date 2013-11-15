#!/bin/env python
import argparse,os,sys
sys.path.extend([os.getenv('CMSSW_BASE')+'/MyCMSSWAnalysisTools/Tools',os.getenv('CMSSW_BASE')+'/MyCMSSWAnalysisTools'])
import tools as myTools
import CrabTools
pwd=os.path.basename(os.getenv("PWD"))
timeSt=myTools.getTimeStamp()
label=pwd+"_LHE2EDM_"+timeSt
parser = argparse.ArgumentParser()
parser.add_argument('--numberOfEvents',type=int,default=-1,help=' number of total events in lhe if not given will be calculated')
parser.add_argument('--remoteDir',type=str,help=' grid dcache dir',required=True)
parser.add_argument('--publishName',type=str,help="name used for publishing",required=True)
parser.add_argument('--lheFile',type=str,help="lhe which will be converted to edm",required=True)
parser.add_argument('--outputFile',type=str,help="output file which will be created",required=True)
#parser.add_argument('--specificSamples',type=str,default=None,help="only process given samples given by labels")
#parser.add_argument('--debug',action='store_true',default=False,help=' activate debug modus ')
args = parser.parse_args()
if not os.path.isfile(args.lheFile):
  print "provided lheFile not found"
  sys.exit(1)
args.lheFile=os.path.realpath(args.lheFile)
numberOfEvents = args.numberOfEvents
if numberOfEvents == -1:
  numberOfEvents = sum(1 for line in open(args.lheFile) if '</event>' in line)
  print "determined ",numberOfEvents," events in ",args.lheFile
import math
eventsPerJob=int(math.floor(numberOfEvents/100))
numberOfJobs=int(math.ceil(numberOfEvents/eventsPerJob))
print "In total ",numberOfEvents," events and ",numberOfJobs," jobs with ",eventsPerJob," events per job will be used"
crabCfgChanges={"CMSSW":{},"USER":{}};  crabCfgChanges["CMSSW"] = {"datasetpath":None, "number_of_jobs":numberOfJobs , "events_per_job":eventsPerJob,"generator":"lhe"}; crabCfgChanges["USER"] = {"additional_input_files":args.lheFile,"publish_data" : 1,"publish_data_name" : label
    ,"dbs_url_for_publication" : "https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet"}
cfgName=label+"_cfg.py"
crabJobDir=os.getenv('PWD')+os.path.sep+pwd+"_LHE2EDM_crabJob_"+timeSt
#print crabJobDir
os.makedirs(crabJobDir)
convertCommand='python $CMSSW_BASE/MCatNLO_Showering/TT_mcatnlo_LHE2EDM_cfg.py inputFiles=file:'+os.path.basename(args.lheFile)+" outputFile="+args.outputFile+" dumpPythonOnly="+crabJobDir+os.path.sep+cfgName
convP=myTools.executeCommandSameEnv(convertCommand)

os.chdir(crabJobDir)
convP.wait()
crabP = CrabTools.crabProcess(pwd,cfgName,None,"crab_LHE2EDM" ,timeSt,addGridDir=args.remoteDir)
crabP.createCrabCfg(crabCfgChanges)
del(crabP.crabCfg['CMSSW']['total_number_of_events'])
crabP.crabDir = crabJobDir
crabP.writeCrabCfg()
crabP.create()
print "lauch with: cd ",crabJobDir,"; crab -submit "
print "saving ..."
crabJsonFile = crabJobDir+os.path.sep+"savedCrabJob_"+timeSt+".json"
CrabTools.saveCrabProp(crabP,crabJsonFile)
