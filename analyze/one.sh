#!/bin/bash
# Run simulation on *.ttt.tsv with one set of parameters, and do analysis.
# Usage: ./one.sh key params..
#   key: prefix of output file names
#   params: passed to nicsim.py

R="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"

KEY=$1
if [[ -z $KEY ]]; then
  echo 'Usage: ./one.sh key params..' >/dev/stderr
  exit 2
fi
shift

PARAMS=''
for PARAM in "$@"; do
  PARAMS="$PARAMS \"${PARAM//\"/\\\"}\""
done

for H in $(ls *.ttt.tsv | sed 's/.ttt.tsv//'); do
  if [[ -f $KEY.$H.nd.tsv ]]; then
    continue
  fi
  PARAMS1=$PARAMS
  PARAMS1=${PARAMS1//KEY/$KEY}
  PARAMS1=${PARAMS1//HOSTNAME/$H}
  echo "python2 $R/nicsim/nicsim.py --comment=$KEY.$H $PARAMS1 < $H.ttt.tsv > $KEY.$H.nd.tsv"
done | $R/analyze/parallelize.sh


if [[ ! -f $KEY.quick-analyze.tsv ]] && [[ -z $NO_QUICK_ANALYZE ]]; then
(
  echo -n host
  echo -ne '\t'
  echo -n nPackets
  echo -ne '\t'
  echo -n nSwAccepts
  echo -ne '\t'
  echo -n nNicAccepts
  echo -ne '\t'
  echo -n nFalsePositives
  echo -ne '\t'
  echo -n nFalseNegatives
  echo

  for H in $(ls *.ttt.tsv | sed 's/.ttt.tsv//'); do
    echo -n $H
    echo -ne '\t'
    echo -n $(cat $KEY.$H.nd.tsv | wc -l)
    echo -ne '\t'
    echo -n $(awk '$4!="DROP"' $KEY.$H.nd.tsv | wc -l)
    echo -ne '\t'
    echo -n $(awk '$5!="DROP"' $KEY.$H.nd.tsv | wc -l)
    echo -ne '\t'
    echo -n $(awk '$4=="DROP" && $5!="DROP"' $KEY.$H.nd.tsv | wc -l)
    echo -ne '\t'
    echo -n $(awk '$4!="DROP" && $5=="DROP"' $KEY.$H.nd.tsv | wc -l)
    echo
  done

) > $KEY.quick-analyze.tsv
fi

if [[ -f $KEY.quick-analyze.tsv ]]; then
  column -t $KEY.quick-analyze.tsv
fi
