#!/bin/bash

./aggregator.py \
    --pos-to-aggregate pos_0b \
    --stat frac_below_lower_thresh \
    --covg covg \
    --region motif \
    --pos-regions pos_0b \
    test/regression_2/files/to_aggregate.csv test/regression_2/files/hiv_regions.csv regression_test_2_ans.csv

exp_hash="$(md5sum test/regression_2/files/exp.csv | awk '{ print $1 }')"
ans_hash="$(md5sum regression_test_2_ans.csv | awk '{ print $1 }')"
if [ "${exp_hash}" = "${ans_hash}" ]; then
    echo "Regression test SUCCESSFUL";
    rm regression_test_2_ans.csv
else
    echo "Regression test FAILED";
    echo "Leaving output file at regression_test_2_ans.csv (if it was created)"
fi;
