#!/bin/bash
# Plot false positive rate as a function of AIT thresholds.
# Usage: ./vary-ait-threshold.sh key thresholds params..
#   key: prefix of output file names
#   thresholds: a TSV file where each line is a tuple of degreeThreshold,fp2Low,fp2High,fp1Low,fp1High,[FIB1|noFIB1];
#               fp thresholds should omit leading "0.";
#               specify <multiplier>x as low limit to have Ait compute low limit automatically
#   params: passed to nicsim.py

R="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"

KEY=$1
THRESHOLDS_FILE=$2
if [[ -z $KEY ]] || [[ ! -r $THRESHOLDS_FILE ]]; then
  echo 'Usage: ./vary-ait-threshold.sh key thresholds params..'
  exit 2
fi
shift 2

PARAMS=''
for PARAM in "$@"; do
  PARAMS="$PARAMS \"${PARAM//\"/\\\"}\""
done

while read -r -a THRESHOLDS; do
  DEGREE=${THRESHOLDS[0]}
  FP2LOW=${THRESHOLDS[1]}
  FP2HIGH=${THRESHOLDS[2]}
  FP1LOW=${THRESHOLDS[3]}
  FP1HIGH=${THRESHOLDS[4]}
  if [[ ${THRESHOLDS[5]} == "FIB1" ]]; then
    KEYFREEFIB1="freeFib1"
    FREEFIB1="useFreeFib1=True"
  else
    KEYFREEFIB1="noFib1"
    FREEFIB1="useFreeFib1=False"
  fi
  KEY1=$KEY.degree-${DEGREE//,/-}_fp2-${FP2LOW}-${FP2HIGH}_fp1-${FP1LOW}-${FP1HIGH}_${KEYFREEFIB1}

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

  echo -n "NO_QUICK_ANALYZE=1 $R/analyze/one.sh $KEY1 --cs=\"AitCs(nic, AitCs.Options($FREEFIB1,degreeThreshold=AitCs.DegreeThreshold($DEGREE), fp2Threshold=$FP2THRESHOLD, fp1Threshold=$FP2THRESHOLD), trace=open('KEY.HOSTNAME.ait-trace.log','w'))\" $PARAMS"

  if [[ ! -f $KEY1.fp-classify.tsv ]]; then
    echo -n " ; gawk -f $R/analyze/fp-classify.awk $KEY1.*.nd.tsv > $KEY1.fp-classify.tsv"
  fi
  echo
done < $THRESHOLDS_FILE | $R/analyze/parallelize.sh

(
  echo -n degree
  echo -ne '\t'
  echo -n fp2low
  echo -ne '\t'
  echo -n fp2high
  echo -ne '\t'
  echo -n fp1low
  echo -ne '\t'
  echo -n fp1high
  echo -ne '\t'
  echo -n freeFib1
  echo -ne '\t'
  echo -n $(echo | gawk -f $R/analyze/fp-classify.awk | head -1)
  echo
) > $KEY.vary-ait-threshold.tsv

while read -r -a THRESHOLDS; do
  DEGREE=${THRESHOLDS[0]}
  FP2LOW=${THRESHOLDS[1]}
  FP2HIGH=${THRESHOLDS[2]}
  FP1LOW=${THRESHOLDS[3]}
  FP1HIGH=${THRESHOLDS[4]}
  if [[ ${THRESHOLDS[5]} == "FIB1" ]]; then
    KEYFREEFIB1="freeFib1"
    FREEFIB1="Y"
  else
    KEYFREEFIB1="noFib1"
    FREEFIB1="N"
  fi
  KEY1=$KEY.degree-${DEGREE//,/-}_fp2-${FP2LOW}-${FP2HIGH}_fp1-${FP1LOW}-${FP1HIGH}_${KEYFREEFIB1}

  tail -n+2 $KEY1.fp-classify.tsv | \
  sed -e "s/^/$DEGREE\t$FP2LOW\t$FP2HIGH\t$FP1LOW\t$FP1HIGH\t$FREEFIB1\t/"
done < $THRESHOLDS_FILE >> $KEY.vary-ait-threshold.tsv

column -t $KEY.vary-ait-threshold.tsv
