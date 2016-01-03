#!/bin/bash
# Plot false positive rate as a function of AIT thresholds.
# Usage: ./vary-ait-threshold.sh key thresholds params..
#   key: prefix of output file names
#   sizes: a TSV file where each line is a tuple of degreeThreshold,fp2Threshold,fp1Threshold
#          fp2Threshold and fp1Threshold should be specified as percentage rather than floating point
#   params: passed to nicsim.py

R="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"

KEY=$1
THRESHOLDS_FILE=$2
if [[ -z $KEY ]] || [[ ! -r $THRESHOLDS_FILE ]]; then
  echo 'Usage: ./vary-ait-threshold.sh key thresholds params..'
  exit 2
fi
shift 2

(
  echo -n degreeThreshold
  echo -ne '\t'
  echo -n fp2Threshold
  echo -ne '\t'
  echo -n fp1Threshold
  echo -ne '\t'
  echo -n host
  echo -ne '\t'
  echo -n $(echo | gawk -f $R/analyze/fp-classify.awk | head -1 | cut -f2-)
  echo
) > $KEY.vary-ait-threshold.tsv

while read -r -a THRESHOLDS; do
  DEGREETHRESHOLD=${THRESHOLDS[0]}
  FP2THRESHOLD=${THRESHOLDS[1]}
  FP1THRESHOLD=${THRESHOLDS[2]}
  KEY1=$KEY.degree-${DEGREETHRESHOLD}_fp2-${FP2THRESHOLD}_fp1-${FP1THRESHOLD}
  $R/analyze/one.sh $KEY1 --cs="AitCs(nic,AitCs.Options(degreeThreshold=$DEGREETHRESHOLD, fp2Threshold=0.01*$FP2THRESHOLD, fp1Threshold=0.01*$FP1THRESHOLD))" "$@" > /dev/null

  gawk -f $R/analyze/fp-classify.awk -v noHeader=1 $KEY1.*.nd.tsv | \
  sed -e "s/$KEY1\.\([^.]*\)\.nd\.tsv/\1/" -e "s/^/$DEGREETHRESHOLD\t$FP2THRESHOLD\t$FP1THRESHOLD\t/"
done < $THRESHOLDS_FILE >> $KEY.vary-ait-threshold.tsv

column -t $KEY.vary-ait-threshold.tsv
