#!/bin/bash
sed -i -e 's/^RMASS(198)\ *=\ *0\ *.*$/RMASS(198)=80.4/g' -e 's/^RMASS(199)\ *=\ *0\ *.*$/RMASS(199)=80.4/g' $@
