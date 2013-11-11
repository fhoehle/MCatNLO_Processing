#!/bin/bash
if [ -z "$CMSSW_BASE" ]; then
  echo "missing cmsenv"
  exit 1
fi
if [ "$1" = "getMCatNLO" ]; then
  cd $CMSSW_BASE
  git clone  git@github.com:MCatNLO-for-CMSSW/MCatNLO_3_4_1.git
  cd  MCatNLO_3_4_1
  ./install.sh
  echo "call source setup.sh in $PWD for MCatNLO usage"
fi
