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

JOBS=${JOBS:-$(grep -c ^processor /proc/cpuinfo)}

for H in $(ls *.ttt.tsv | sed 's/.ttt.tsv//'); do
  if [[ -f $KEY.$H.nd.tsv ]]; then
    continue
  fi
  while [[ $(jobs -p | wc -l) -ge $JOBS ]]; do
    sleep 0.1
  done
  python2 $R/nicsim/nicsim.py "$@" < $H.ttt.tsv > $KEY.$H.nd.tsv &
done
wait

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

column -t $KEY.analyze.tsv
