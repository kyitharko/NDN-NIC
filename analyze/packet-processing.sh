#!/bin/bash
# Esimate packet processing overhead based on NIC decision.
# Usage: ./packet-processing.sh key

R="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"

KEY=$1
if [[ -z $KEY ]]; then
  echo 'Usage: ./packet-processing.sh key' >/dev/stderr
  exit 2
fi

for H in $(ls *.ttt.tsv | sed 's/.ttt.tsv//'); do
  if [[ -f $H.packet-processing.tsv ]]; then
    continue
  fi
  python2 $R/nicsim/packet_processing.py < $H.ttt.tsv > $H.packet-processing.tsv
done

for KEY1 in $(ls $KEY.*.nd.tsv.xz | awk 'BEGIN { FS=OFS="." } { NF-=4; print }' | sort | uniq); do
  echo -n $(echo $KEY1 | cut -d. -f2-)
  echo -ne '\t'

  if ! [[ -f $KEY1.packet-processing-subtotal.tsv ]]; then
    for H in $(ls *.ttt.tsv | sed 's/.ttt.tsv//'); do
      echo -n $H
      echo -ne '\t'
      xzcat $KEY1.$H.nd.tsv.xz | paste - $H.packet-processing.tsv | \
      awk 'BEGIN { FS="\t"; v=0 } $5 != "DROP" { v+=$10 } END { print v }'
    done > $KEY1.packet-processing-subtotal.tsv
  fi
  echo -n $(awk 'BEGIN { FS="\t" } { sum+=$2 } END { print sum }' $KEY1.packet-processing-subtotal.tsv)

  AITTRACES=($KEY1.*.ait-trace.log.xz)
  if [[ -f "${AITTRACES[0]}" ]]; then
    echo -ne '\t'
    if [[ -f $KEY1.ait-computation.tsv ]]; then
      echo -n $(awk 'BEGIN { FS="\t" } NR>1 { sum+=$6 } END { print sum }' $KEY1.ait-computation.tsv)
    else
      echo -n 'MISSING'
    fi
  fi

  echo
done
