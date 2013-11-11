#!/bin/env python
import argparse,os,sys
sys.path.extend([os.getenv('CMSSW_BASE')+'/MyCMSSWAnalysisTools/Tools',os.getenv('CMSSW_BASE')+'/MyCMSSWAnalysisTools'])
import tools as myTools
import CrabTools
pwd=os.path.basename(os.getenv("PWD"))
timeSt=myTools.getTimeStamp()
parser = argparse.ArgumentParser()
parser.add_argument('--numberOfEvents',type=int,default=-1,help=' number of total events in lhe if not given will be calculated')
parser.add_argument('--remoteDir',type=str,help=' grid dcache dir',required=True)
parser.add_argument('--publishName',type=str,help="name used for publishing",required=True)
parser.add_argument('--lheFile',type=str,help="lhe which will be converted to edm",required=True)
parser.add_argument('--outputFile',type=str,help="output file which will be created",required=True)
#parser.add_argument('--specificSamples',type=str,default=None,help="only process given samples given by labels")
#parser.add_argument('--debug',action='store_true',default=False,help=' activate debug modus ')
args = parser.parse_args()
cfgName=pwd+"_LHE2EDM_"+timeSt+"_cfg.py"
convertCommand='python $CMSSW_BASE/MCatNLO_Showering/TT_mcatnlo_LHE2EDM_cfg.py inputFiles=file:'+args.lheFile+" outputFile="+args.outputFile+" dumpPythonOnly="+cfgName
myTools.executeCommandSameEnv(convertCommand)
crabP = CrabTools.crabProcess("",cfgName,None,"crab_LHE2EDM" ,timeSt,addGridDir=args.remoteDir)
