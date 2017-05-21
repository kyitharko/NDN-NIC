#!/bin/bash
# Estimate packet processing overhead based on NIC decision.
# AIT computation overhead is also listed if available.
# Usage: ./packet-processing.sh key

R="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"

KEY=$1
if [[ -z $KEY ]]; then
  echo 'Usage: ./packet-processing.sh key' >/dev/stderr
  exit 2
fi

if ! find *.packet-processing-base.tsv.xz >&/dev/null; then
  echo 'Run packet-processing-base.sh first.' >/dev/stderr
  exit 1
fi

for KEY1 in $(ls $KEY.*.nd.tsv.xz | awk 'BEGIN { FS=OFS="." } { NF-=4; print }' | sort | uniq); do
  echo -n $(echo $KEY1 | cut -d. -f2-)
  echo -ne '\t'

  if ! [[ -f $KEY1.packet-processing-subtotal.tsv ]]; then
    for H in $(ls *.ttt.tsv.xz | sed 's/.ttt.tsv.xz//'); do
      echo -n $H
      echo -ne '\t'
      paste <(xzcat $KEY1.$H.nd.tsv.xz) <(xzcat $H.packet-processing-base.tsv.xz) | \
      awk 'BEGIN { FS="\t"; v=0 } $6!="DROP" { v+=$12 } END { print v }'
    done > $KEY1.packet-processing-subtotal.tsv
  fi
  echo -n $(awk 'BEGIN { FS="\t" } { sum+=$2 } END { print sum }' $KEY1.packet-processing-subtotal.tsv)

  if find $KEY1.*.ait-trace.log.xz >&/dev/null; then
    echo -ne '\t'
    if [[ -f $KEY1.ait-computation.tsv ]]; then
      echo -n $(awk 'BEGIN { FS="\t" } NR>1 { sum+=$6 } END { print sum }' $KEY1.ait-computation.tsv)
    else
      echo -n 'MISSING'
    fi
  fi

  echo
done | column -t
