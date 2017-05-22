# run experiments for teaser/bfsize/csalgo plot

export BF1EXTRA=,xor,../bf1.poly
export BF2EXTRA=,xor,../bf2.poly
export BF3EXTRA=,xor,../bf3.poly
export JOBS=24x1

$NDNNICROOT/analyze/packet-processing-base.sh

$NDNNICROOT/analyze/vary-bf-size.sh direct ../bfsize.tsv --cs=DirectCs

$NDNNICROOT/analyze/vary-bf-size.sh basic ../bfsize.tsv --cs=BasicCs

ACTIVEKEY=active_degree-64-64-32-16_fp2-2x-001_fp1-2x-001
$NDNNICROOT/analyze/vary-bf-size.sh $ACTIVEKEY ../bfsize.tsv --cs="ActiveCs(nic,ActiveCs.Options(degreeThreshold=ActiveCs.DegreeThreshold(64,64,32,16),fp2Threshold=(None,0.001,2),fp1Threshold=(None,0.001,2)),trace=open('KEY.HOSTNAME.ait-trace.log','w'))"
for F in $ACTIVEKEY.*.ait-trace.log; do echo xz $F; done | $NDNNICROOT/analyze/parallelize.sh

for KEY in $(ls $ACTIVEKEY.*.nd.tsv.xz | cut -d. -f1-2 | sort -u); do
  echo "ls $KEY.*.ait-trace.log.xz | gawk -f $NDNNICROOT/analyze/ait-computation.awk > $KEY.ait-computation.tsv"
done | $NDNNICROOT/analyze/parallelize.sh

(
  echo $NDNNICROOT/analyze/packet-processing.sh direct
  echo $NDNNICROOT/analyze/packet-processing.sh basic
  echo $NDNNICROOT/analyze/packet-processing.sh $ACTIVEKEY
) | $NDNNICROOT/analyze/parallelize.sh
