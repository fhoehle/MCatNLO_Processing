#!/bin/bash

pwdName=${PWD##*/}
if [ "$1" = "GEN-SIM42" ]; then
  fileIn="test_LHE2EDM.root"
  if [ ! "X$2" = "X" ]; then
    fileIn=$2
  fi
  fileOut="test_GEN-SIM42.root"
    if [ ! "X$3" = "X" ]; then
    fileOut=$3
  fi
  cmsDriver.py Configuration/MyGenProduction/python/TT_7TeV_mcatnlo_cff.py --step GEN,SIM --beamspot Realistic7TeV2011Collision --conditions START42_V14B::All --pileup NoPileUp --datamix NODATAMIXER --eventcontent RAWSIM --datatier GEN-SIM --filein file:$fileIn --fileout $fileOut --python_filename TT_MCatNLO_${pwdName}_START42_V14B_GEN-SIM_cfg.py --no_exec -n -1
fi

if [ "$1" = "AODSIM42" ]; then
  fileIn="test_GEN-SIM42.root"
  if [ ! "X$2" = "X" ]; then
    fileIn=$2
  fi
  fileOut="test_AODSIM42.root"
    if [ ! "X$3" = "X" ]; then
    fileOut=$3
  fi
  cmsDriver.py REDIGI --step DIGI,L1,DIGI2RAW,HLT,RAW2DIGI,RECO --conditions auto:startup --pileup mix_E7TeV_Fall2011_Reprocess_50ns_PoissonOOTPU_cfi --datamix NODATAMIXER --eventcontent AODSIM --datatier AODSIM --filein file:$fileIn --fileout $fileOut --python_filename TT_MCatNLO_${pwdName}_START42_V14B_ADOSIM_cfg.py --no_exec -n -1
fi


