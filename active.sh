# run experiments for fpthresholds/degree plot

export BF1EXTRA=,xor,../bf1.poly
export BF2EXTRA=,xor,../bf2.poly
export BF3EXTRA=,xor,../bf3.poly
export JOBS=4x1x10

$NDNNICROOT/analyze/vary-ait-threshold.sh ../active.fpthres.tsv ../active.bfsize.tsv

# TODO tailored degree threshold
