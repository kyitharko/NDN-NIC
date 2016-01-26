#!/bin/bash
# Run simulation on *.ttt.tsv with one set of parameters, and do quick analysis.
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
  if [[ -f $KEY.$H.nd.tsv.xz ]]; then
    continue
  fi
  PARAMS1=$PARAMS
  PARAMS1=${PARAMS1//KEY/$KEY}
  PARAMS1=${PARAMS1//HOSTNAME/$H}
  echo "python2 $R/nicsim/nicsim.py --comment=$KEY.$H $PARAMS1 < $H.ttt.tsv | xz > $KEY.$H.nd.tsv.xz"
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
    xzcat $KEY.$H.nd.tsv.xz | awk '
    BEGIN { OFS = "\t" }
    { ++nPackets }
    $4 != "DROP" { ++nSwAccepts }
    $5 != "DROP" { ++nNicAccepts }
    $4 == "DROP" && $5 != "DROP" { ++nFalsePositives }
    $4 != "DROP" && $5 == "DROP" { ++nFalseNegatives }
    END { print 0 + nPackets, 0 + nSwAccepts, 0 + nNicAccepts, 0 + nFalsePositives, 0 + nFalseNegatives }
    '
  done
) > $KEY.quick-analyze.tsv
fi

if [[ -f $KEY.quick-analyze.tsv ]]; then
  column -t $KEY.quick-analyze.tsv
fi
