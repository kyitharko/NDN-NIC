#!/bin/bash
# Collect packet bytes and number of BF update commands.
# Usage: ./bfu.sh

R="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"

AHOST=$(ls *.ttt.tsv.xz | sed 's/.ttt.tsv.xz//' | head -1)

for PREFIX in $(ls *.$AHOST.bfu.tsv.xz | sed 's/.'$AHOST'.bfu.tsv.xz//' | sort -u); do
  if [[ -f $PREFIX.bfu-stats.tsv ]]; then
    continue
  fi
  echo "ls *.ttt.tsv.xz | sed 's/.ttt.tsv.xz//' | $R/analyze/bfu-one.awk -v PREFIX=$PREFIX > $PREFIX.bfu-stats.tsv"
done | $R/analyze/parallelize.sh
