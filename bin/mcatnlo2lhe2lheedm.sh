#! /bin/bash
#######################
## check if CMSSW environment is available and MCatNLO_Showering and MCatNLO2LHE are installed correctly
if [ -z $CMSSW_BASE ] || [ ! -d $CMSSW_BASE/MCatNLO2LHE ] || [ ! -d $CMSSW_BASE/MCatNLO_Showering ]; then
  echo "CMSSW_BASE missing i.e. cmsenv not executed or MCatNLO2LHE and or MCATNLO_Showering not installed"
  exit 1
fi
### 
function usage()
{
  echo -e "Script to convert mcatnlo output to lhe and edm.
           Options:
           --onlyLHE convert mcatnlo to lhe don't convert further to edm
           --notest don't test resulting lhe
           --input <inputMcatnlo>
           --noMCatNLOinputs MCatNLO.inputs are not added to LHE header
           --outputLHE <outputLHE file>
           --outputEDM <outputEDM file>
           -h print this help\n" 1>&2
}
##setup standard values of variables
#### get input from MCatNLO.inputs
if [ -f MCatNLO.inputs ]; then 
  postfix=`cat MCatNLO.inputs | grep EVPREFIX | sed 's/.*=\ *\([^=\ ]*\)[\ \$]*.*/\1/'`
else 
  echo "warning: no MCatNLO.inputs found, you should provide it or use input option"
fi
input="Linux/$postfix.events"
filenamePrefix=${PWD##*/}
outputLHE=${filenamePrefix}.lhe
outputEDM=${filenamePrefix}_LHE2EDM
## read from commandline
while [ $# -ge 1 ]; do
  case $1 in
    --onlyLHE ) onlyLHE=true; shift ;;
    --notest ) notest=true; shift ;;
    --noMCatNLOinputs ) noMCatNLOinputs=true; shift ;;
    --input ) input=$2; shift 2;;
    --outputLHE ) outputLHE=$2; shift 2;;
    --outputEDM ) outputEDM=$2; shift 2;;
    -h ) usage 1>&2; exit 1 ;;
    --help ) usage 1>&2; exit 1 ;;
    * ) echo "$0: unrecognised option $1, use -h for help" 1>&2; exit 1 ;;
  esac
done
### check input
if [ ! -f $input ]; then
    echo "input not found: $input is not existing"
    exit 1
fi
## MCatNLO to LHE
mcatnlo2lheCommand="cmsRun $CMSSW_BASE/MCatNLO2LHE/convertMCatNLO2LHE_cfg.py inputFiles=file:$input mcatnloInputsFile=MCatNLO.inputs outputFile=$outputLHE >& converting_mcatnlo2edm_${filenamePrefix}_log.txt"
echo "$mcatnlo2lheCommand"
eval $mcatnlo2lheCommand
#renaming
mv ${outputLHE}.root $outputLHE
#
if [ "x$notest" != "xtrue" ]; then
  echo "testing lhe"
  testLHEcmd="cmsDriver.py lhetest --filein file:$outputLHE --mc --conditions auto:startup -n -1 --python lhetest_${filenamePrefix}.py --step NONE --no_output  >& lhetest_${filenamePrefix}.py_log.txt"
  echo "$testLHEcmd"
  eval $testLHEcmd
  if [ "$?" != "0" ]; then
    echo "lhe contains errors, see lhetest_${filenamePrefix}.py_log.txt"
    exit 1 
  fi
fi
## adding mcatnlo.inputs
if [ "x$noMCatNLOinputs" != "xtrue" ]; then 
  cmd="python $CMSSW_BASE/MCatNLO2LHE/addMCatNLOinputsToLHEfile.py --lheFile $outputLHE --mcatnloInputs MCatNLO.inputs"
  echo $cmd
  eval $cmd
  if [ "x$notest" != "xtrue" ]; then
    echo "testing lhe"
    testLHEcmd="cmsDriver.py lhetest --filein file:$outputLHE --mc --conditions auto:startup -n -1 --python lhetest_${filenamePrefix}.py --step NONE --no_output >& lhetest_${filenamePrefix}.py_withMCatnlo.inputs_log.txt "
    echo "$testLHEcmd"
    eval $testLHEcmd
    if [ "$?" != "0" ]; then
      echo "lhe contains errors, see lhetest_${filenamePrefix}.py_withMCatnlo.inputs_log.txt"
      exit 1
    fi
  fi
fi
# LHE2EDM
if [ "x$onlyLHE" != "xtrue" ]; then
  echo "converting from LHE 2 EDM"
  lhe2edmCommand="cmsRun $CMSSW_BASE/MCatNLO_Showering/TT_mcatnlo_LHE2EDM_cfg.py inputFiles=file:$outputLHE outputFile=$outputEDM >& ${filenamePrefix}_LHE2EDM_cfg.py_log.txt"
  echo "$lhe2edmCommand"
  eval $lhe2edmCommand
fi
