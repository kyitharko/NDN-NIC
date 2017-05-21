#!/bin/bash
# Estimate baseline packet processing overhead if NIC accepts packet.
# Usage: ./packet-processing-base.sh

R="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"

for H in $(ls *.ttt.tsv.xz | sed 's/.ttt.tsv.xz//'); do
  echo "xzcat $H.ttt.tsv.xz | python2 $R/nicsim/packet_processing.py | xz > $H.packet-processing-base.tsv.xz"
done | $R/analyze/parallelize.sh
