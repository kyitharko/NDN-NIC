#!/bin/bash
# Plot false positive rate as a function of AIT thresholds.
# Usage: ./vary-ait-threshold.sh key thresholds params..
#   key: prefix of output file names
#   sizes: a TSV file where each line is a tuple of degreeThreshold,fp2Low,fp2High,fp1Low,fp1High;
#          fp thresholds should omit leading "0.";
#          specify <multiplier>x as low limit to have Ait compute low limit automatically
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
  echo -n DEGREE
  echo -ne '\t'
  echo -n FP2LOW
  echo -ne '\t'
  echo -n FP2HIGH
  echo -ne '\t'
  echo -n FP1LOW
  echo -ne '\t'
  echo -n FP1HIGH
  echo -ne '\t'
  echo -n HOST
  echo -ne '\t'
  echo -n $(echo | gawk -f $R/analyze/fp-classify.awk | head -1 | cut -f2-)
  echo
) > $KEY.vary-ait-threshold.tsv

while read -r -a THRESHOLDS; do
  DEGREE=${THRESHOLDS[0]}
  FP2LOW=${THRESHOLDS[1]}
  FP2HIGH=${THRESHOLDS[2]}
  FP1LOW=${THRESHOLDS[3]}
  FP1HIGH=${THRESHOLDS[4]}
  KEY1=$KEY.degree-${DEGREE}_fp2-${FP2LOW}-${FP2HIGH}_fp1-${FP1LOW}-${FP1HIGH}

  if [[ $FP2LOW == *x ]]; then
    FP2THRESHOLD="(None,0.$FP2HIGH,${FP2LOW::-1})"
  else
    FP2THRESHOLD="(0.$FP2LOW,0.$FP2HIGH)"
  fi
  if [[ $FP1LOW == *x ]]; then
    FP1THRESHOLD="(None,0.$FP1HIGH,${FP1LOW::-1})"
  else
    FP1THRESHOLD="(0.$FP1LOW,0.$FP1HIGH)"
  fi

  NO_QUICK_ANALYZE=1 $R/analyze/one.sh $KEY1 --cs="AitCs(nic, AitCs.Options(degreeThreshold=$DEGREE, fp2Threshold=$FP2THRESHOLD, fp1Threshold=$FP2THRESHOLD))" "$@"

  if [[ ! -f $KEY1.fp-classify.tsv ]]; then
    gawk -f $R/analyze/fp-classify.awk $KEY1.*.nd.tsv > $KEY1.fp-classify.tsv
  fi
  tail -n+2 $KEY1.fp-classify.tsv | \
  sed -e "s/$KEY1\.\([^.]*\)\.nd\.tsv/\1/" -e "s/^/$DEGREE\t$FP2LOW\t$FP2HIGH\t$FP1LOW\t$FP1HIGH\t/"
done < $THRESHOLDS_FILE >> $KEY.vary-ait-threshold.tsv

column -t $KEY.vary-ait-threshold.tsv
