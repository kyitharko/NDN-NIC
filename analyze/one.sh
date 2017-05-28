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

for H in $(ls *.ttt.tsv.xz | sed 's/.ttt.tsv.xz//'); do
  if [[ -f $KEY.$H.nd.tsv.xz ]] && [[ -f $KEY.$H.bfu.tsv.xz ]]; then
    continue
  fi
  PARAMS1=$PARAMS
  PARAMS1=${PARAMS1//KEY/$KEY}
  PARAMS1=${PARAMS1//HOSTNAME/$H}
  echo "xzcat $H.ttt.tsv.xz | python2 $R/nicsim/nicsim.py --comment=$KEY.$H $PARAMS1 --nd >(xz > $KEY.$H.nd.tsv.xz) --bfu >(xz > $KEY.$H.bfu.tsv.xz)"
done | $R/analyze/parallelize.sh

if find $KEY.*.ait-trace.log >&/dev/null; then
  for F in $KEY.*.ait-trace.log; do echo xz $F; done | $NDNNICROOT/analyze/parallelize.sh
fi
if find $KEY.*.ait-trace.log.xz >&/dev/null && ! [[ -f $KEY.ait-computation.tsv ]]; then
  ls $KEY.*.ait-trace.log.xz | $NDNNICROOT/analyze/ait-computation.awk > $KEY.ait-computation.tsv
fi

if ! [[ -f $KEY.ntnode-access.tsv ]]; then
  for H in $(ls *.ttt.tsv.xz | sed 's/.ttt.tsv.xz//'); do
    echo "paste <(xzcat $KEY.$H.nd.tsv.xz) <(xzcat $H.packet-processing-base.tsv.xz) | awk 'BEGIN { FS=\"\\t\"; v=0 } \$6!=\"DROP\" { v+=\$12 } END { print v }' >$KEY.$H.packet-processing.sum.txt"
  done | $R/analyze/parallelize.sh
  AITFILE=$KEY.ait-computation.tsv
  if ! [[ -f $AITFILE ]]; then
    AITFILE=/dev/null
  fi
  ls *.ttt.tsv.xz | sed 's/.ttt.tsv.xz//' | awk '
    BEGIN {
      OFS = "\t"
      print "HOST", "PKT-PROC", "AIT", "TOTAL"

      while ((getline < "'$AITFILE'") > 0) {
        aits[$1] == $4
      }
      aits["+"] = 0

      totalPktProc = 0
      totalAit = 0
    }
    {
      getline pktProc < ("'$KEY'." $1 ".packet-processing.sum.txt")
      ait = 0 + aits[$1]
      print $1, pktProc, ait, (pktProc+ait)

      totalPktProc += pktProc
      totalAit += ait
    }
    END {
      print "+", totalPktProc, totalAit, (totalPktProc+totalAit)
    }
  ' > $KEY.ntnode-access.tsv
  rm $KEY.*.packet-processing.sum.txt
fi

if ! [[ -f $KEY.quick-analyze.tsv ]]; then
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
  echo -ne '\t'
  echo -n nTableChanges
  echo -ne '\t'
  echo -n nBfUpdates
  echo

  for H in $(ls *.ttt.tsv.xz | sed 's/.ttt.tsv.xz//'); do
    echo -n $H
    echo -ne '\t'
    xzcat $KEY.$H.nd.tsv.xz | awk '
    BEGIN { OFS = "\t"; ORS = "" }
    { ++nPackets }
    $5 != "DROP" { ++nSwAccepts }
    $6 != "DROP" { ++nNicAccepts }
    $5 == "DROP" && $6 != "DROP" { ++nFalsePositives }
    $5 != "DROP" && $6 == "DROP" { ++nFalseNegatives }
    END { print 0 + nPackets, 0 + nSwAccepts, 0 + nNicAccepts, 0 + nFalsePositives, 0 + nFalseNegatives }
    '
    echo -ne '\t'
    xzcat $KEY.$H.bfu.tsv.xz | awk '
    BEGIN { OFS = "\t"; ORS = "" }
    { ++nTableChanges }
    $5 != 0 || $6 != 0 || $7 != 0 || $8 != 0 || $9 != 0 || $10 != 0 { ++nBfUpdates }
    END { print 0 + nTableChanges, 0 + nBfUpdates }
    '
    echo
  done
) > $KEY.quick-analyze.tsv
fi

column -t $KEY.quick-analyze.tsv
