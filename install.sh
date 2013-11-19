#! /bin/bash
## install MCatNLO_Showering
if [ -z "$CMSSW_BASE" ]; then
  exit "set CMSSW_BASE or execute cmsenv"
fi
cd $CMSSW_BASE
git clone git@github.com:fhoehle/MCatNLO_Showering.git
cd MCatNLO_Showering
if [ -f install.sh  ]; then
  ./install.sh
fi
cd $CMSSW_BASE
git clone git@github.com:fhoehle/MCatNLO2LHE.git
cd MCatNLO2LHE
if [ -f install.sh  ]; then
  ./install.sh
fi

mkdir $CMSSW_BASE/src/Configuration
cd $CMSSW_BASE/src/Configuration
git clone git@github.com:fhoehle/MyGenProduction.git
scram b
cd $CMSSW_BASE

