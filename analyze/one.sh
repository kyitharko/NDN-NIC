#!/bin/bash
# Run simulation on *.ttt.tsv with one set of parameters, and do analysis.
# Usage: ./one.sh <key> <params>
# Output files are named with <key>.
# <params> are passed to nicsim.py.

NDNNIC_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"
NICSIM_PY=$NDNNIC_ROOT/nicsim/nicsim.py

KEY=$1
if [[ -z $KEY ]]; then
  echo 'Usage: ./one.sh <key> <params>'
  exit 1
fi
shift

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
) > $KEY.analyze.tsv

for H in $(ls *.ttt.tsv | sed 's/.ttt.tsv//'); do
  python2 $NICSIM_PY "$@" < $H.ttt.tsv > $KEY.$H.nd.tsv

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
done >> $KEY.analyze.tsv
