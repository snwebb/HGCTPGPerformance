#!/bin/bash

while getopts i:o: option
do
        case "${option}"
        in
                i) INPUT=$OPTARG;;
                o) OUTPUT=$OPTARG;;
        esac
done

#cd res/
#tar -cf ${INPUT}.tar.gz ${INPUT}
rsync -qar res/${INPUT}/ntuple_jet*root snwebb@lx00.hep.ph.ic.ac.uk:/vols/cms/snwebb/HGC_ntuples/${OUTPUT}/jet_ntuples/.





