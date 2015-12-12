#!/bin/bash
# Plot false positive rate as a function of Bloom filter size.
# Usage: ./vary-bf-size.sh key sizes params..
#   key: prefix of output file names
#   sizes: a TSV file where each line is a tuple of BF1,BF2 size
#   params: passed to nicsim.py

R="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"

KEY=$1
SIZES_FILE=$2
if [[ -z $KEY ]] || [[ ! -r $SIZES_FILE ]]; then
  echo 'Usage: ./vary-bf-size.sh key sizes params..'
  exit 2
fi
shift 2

(
  echo -n bf1size
  echo -ne '\t'
  echo -n bf2size
  echo -ne '\t'
  echo -n host
  echo -ne '\t'
  echo -n nNicAccepts
  echo -ne '\t'
  echo -n nFalsePositives
  echo -ne '\t'
  echo -n fpRate # nFalsePositives/nSwAccepts
  echo
) > $KEY.vary-by-size.tsv

while read -r -a SIZES; do
  BF1SIZE=${SIZES[0]}
  BF2SIZE=${SIZES[1]}
  KEY1=$KEY.bf1-${BF1SIZE}_bf2-${BF2SIZE}
  $R/analyze/one.sh $KEY1 --bf1=$BF1SIZE --bf2=$BF2SIZE "$@" > /dev/null

  awk '
  BEGIN {
    totalNicAccepts = 0
    totalFalsePositives = 0
  }
  NR > 1 {
    totalNicAccepts += $4
    totalFalsePositives += $5
    print '$BF1SIZE', '$BF2SIZE', $1, $4, $5,
          $4==0 ? 0 : $5/$4
  }
  END {
    print '$BF1SIZE', '$BF2SIZE', "+", totalNicAccepts, totalFalsePositives,
          totalNicAccepts==0 ? 0 : totalFalsePositives/totalNicAccepts
  }
  ' $KEY1.analyze.tsv
done < $SIZES_FILE >> $KEY.vary-by-size.tsv

column -t $KEY.vary-by-size.tsv
