#! /bin/bash
if [ "$1" == "-h" ]  || [ "$1" == "--help" ]; then
    echo "Usage: `basename $0` [-h] [--onlyLHE]"
    exit 0
fi
postfix=""
if [ -z $CMSSW_BASE ] || [ ! -d $CMSSW_BASE/MCatNLO2LHE ] || [ ! -d $CMSSW_BASE/MCatNLO_Showering ]; then
  echo "CMSSW_BASE missing i.e. cmsenv not executed or MCatNLO2LHE not installed"
  exit 1
fi
inputFile="Linux/$postfix.events"
optionalInput=${BASH_ARGV[0]}
if [ -f MCatNLO.inputs ]; then 
  postfix=`cat MCatNLO.inputs | grep EVPREFIX | sed 's/.*=\ *\([^=\ ]*\)[\ \$]*.*/\1/'`
  if [ ! -f $inputFile ] && [ ! -f $optionalInput ]; then
    echo "no mcatnlo output found: $inputFile"
    exit 1
  fi
  else 
    echo "not MCatNLO.inputs found"
    exit 1
fi
pwdName=${PWD##*/}
echo "converting mcatnlo output to lhe"
if [ ! -f $inputFile ]; then
  inputFile=$optionalInput
fi
mcatnlo2lheCommand="cmsRun $CMSSW_BASE/MCatNLO2LHE/convertMCatNLO2LHE_cfg.py inputFiles=file:$inputFile mcatnloInputsFile=MCatNLO.inputs outputFile=$pwdName.lhe >& converting_mcatnlo2edm_${pwdName}_log.txt"
echo "$mcatnlo2lheCommand"
eval $mcatnlo2lheCommand
#renaming
mv $pwdName.lhe.root $pwdName.lhe
## adding mcatnlo.inputs
cmd="python $CMSSW_BASE/MCatNLO2LHE/addMCatNLOinputsToLHEfile.py --lheFile $pwdName.lhe --mcatnloInputs MCatNLO.inputs"
echo $cmd
eval $cmd
# LHE2EDM
if [[ "$1" == "--onlyLHE" ]]; then
  exit 0 
fi
echo "converting from LHE 2 EDM"
lhe2edmCommand="cmsRun $CMSSW_BASE/MCatNLO_Showering/TT_mcatnlo_LHE2EDM_cfg.py inputFiles=file:$pwdName.lhe outputFile=${pwdName}_LHE2EDM >& lhe2edm_${pwdName}_log.txt"
echo "$lhe2edmCommand"
eval $lhe2edmCommand
