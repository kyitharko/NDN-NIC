#!/bin/bash
# Plot false positive rate as a function of Bloom filter size.
# Usage: ./vary-bf-size.sh key sizes params..
#   key: prefix of output file names
#   sizes: a TSV file where each line is a tuple of BF-FIB,BF-CS,BF-PIT size
#   params: passed to nicsim.py

R="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"

KEY=$1
SIZES_FILE=$2
BFSIZE_REPORT_TAG=${BFSIZE_REPORT_TAG:-bfsize}
if [[ -z $KEY ]] || [[ ! -r $SIZES_FILE ]]; then
  echo 'Usage: ./vary-bf-size.sh key sizes params..'
  exit 2
fi
shift 2

PARAMS=''
for PARAM in "$@"; do
  PARAMS="$PARAMS \"${PARAM//\"/\\\"}\""
done

while read -r -a SIZES; do
  BF1SIZE=${SIZES[0]}
  BF2SIZE=${SIZES[1]}
  BF3SIZE=${SIZES[2]}
  KEY1=$KEY.bf-${BF1SIZE}-${BF2SIZE}-${BF3SIZE}
  echo "$R/analyze/one.sh $KEY1 --bf1=$BF1SIZE$BF1EXTRA --bf2=$BF2SIZE$BF2EXTRA --bf3=$BF3SIZE$BF3EXTRA $PARAMS >/dev/null"
done < $SIZES_FILE | $R/analyze/parallelize.sh

(
  echo -n BF-FIB
  echo -ne '\t'
  echo -n BF-CS
  echo -ne '\t'
  echo -n BF-PIT
  echo -ne '\t'
  head -1 $(find $KEY.*.ntnode-access.tsv | head -1)

  while read -r -a SIZES; do
    BF1SIZE=${SIZES[0]}
    BF2SIZE=${SIZES[1]}
    BF3SIZE=${SIZES[2]}
    KEY1=$KEY.bf-${BF1SIZE}-${BF2SIZE}-${BF3SIZE}

    tail -n+2 $KEY1.ntnode-access.tsv | \
    sed -e "s/^/$BF1SIZE\t$BF2SIZE\t$BF3SIZE\t/"
  done < $SIZES_FILE
) > $KEY.$BFSIZE_REPORT_TAG.tsv

column -t $KEY.$BFSIZE_REPORT_TAG.tsv
