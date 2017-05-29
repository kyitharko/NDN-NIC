#!/bin/bash
# Plot max-degree from TTT.
# Usage: ./max-degree.sh

R="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"

for H in $(ls *.ttt.tsv.xz | sed 's/.ttt.tsv.xz//'); do
  if [[ -f $H.max-degree.tsv.xz ]]; then
    continue
  fi
  echo "xzcat $H.ttt.tsv.xz | python2 $R/nicsim/max_degree.py --comment=$H | xz > $H.max-degree.tsv.xz"
done | $R/analyze/parallelize.sh

xzcat *.max-degree.tsv.xz \
| sort -k2n -k3n \
| gawk '
function printSubtotal() {
  if (nComponents == -1) {
    return
  }
  avg = sum/cnt
  min = vector[0]
  max = vector[cnt-1]
  mean = vector[int(cnt*0.50)]
  percentile90 = vector[int(cnt*0.90)]
  percentile95 = vector[int(cnt*0.95)]
  print nComponents, cnt, avg, min, max, mean, percentile90, percentile95
}
BEGIN {
  FS = OFS = "\t"
  nComponents = 0
  sum = cnt = 0
  print "nComponents", "cnt", "avg", "min", "max", "mean", "percentile90", "percentile95"
}
$2 != nComponents {
  printSubtotal()
  nComponents = $2
  sum = cnt = 0
  delete vector
}
{
  vector[cnt] = $3
  ++cnt
  sum += $3
}
END {
  printSubtotal()
}
' > max-degree-subtotals.tsv
