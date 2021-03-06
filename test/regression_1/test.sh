#!/bin/bash

./aggregator.py \
    --pos-to-aggregate pos_0b \
    --stat num_below_lower_thresh \
    --covg covg \
    --region region_colname \
    --pos-regions pos \
    test/regression_1/files/to_aggregate.csv \
    test/regression_1/files/regions.csv \
    regression_test_1_ans.csv

exp_hash="$(md5sum test/regression_1/files/exp.csv | awk '{ print $1 }')"
ans_hash="$(md5sum regression_test_1_ans.csv | awk '{ print $1 }')"
if [ "${exp_hash}" = "${ans_hash}" ]; then
    echo "Regression test SUCCESSFUL";
    rm regression_test_1_ans.csv
else
    echo "Regression test FAILED";
    echo "Leaving output file at regression_test_1_ans.csv (if it was created)"
fi;
