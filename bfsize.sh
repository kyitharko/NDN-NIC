# run experiments for teaser/bfsize/csalgo plot

export BF1EXTRA=,xor,../bf1.poly
export BF2EXTRA=,xor,../bf2.poly
export BF3EXTRA=,xor,../bf3.poly
export JOBS=24x1

$NDNNICROOT/analyze/vary-bf-size.sh direct ../bfsize.tsv --cs=DirectCs

$NDNNICROOT/analyze/vary-bf-size.sh basic ../bfsize.tsv --cs=BasicCs

ACTIVEKEY=active_degree-64-32-16_fp2-2x-001_fp1-2x-001
$NDNNICROOT/analyze/vary-bf-size.sh $ACTIVEKEY ../bfsize.tsv --cs="ActiveCs(nic,ActiveCs.Options(degreeThreshold=ActiveCs.DegreeThreshold(64,32,16),fp2Threshold=(None,0.001,2),fp1Threshold=(None,0.001,2)),trace=open('KEY.HOSTNAME.ait-trace.log','w'))"
