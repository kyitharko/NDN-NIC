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
  percentile80 = vector[int(cnt*0.80)]
  percentile90 = vector[int(cnt*0.90)]
  print nComponents, cnt, avg, min, max, mean, percentile80, percentile90
}
BEGIN {
  FS = OFS = "\t"
  nComponents = 0
  sum = cnt = 0
  print "nComponents", "cnt", "avg", "min", "max", "mean", "percentile80", "percentile90"
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

YMAX=$(cut -f5 max-degree-subtotals.tsv | sort -nr | head -1)

if ! which gnuplot >/dev/null; then
  echo 'Skipping plotting: gnuplot is unavailable.' >/dev/stderr
  exit
fi

gnuplot -e '
set term pdfcairo dashed font ",20";
set out "max-degree-subtotals.pdf";

set border 3;
set xtics nomirror;
set ytics nomirror;

set yrange [0:'$YMAX'];
set xlabel "nComponents";
set ylabel "maxDegree";

plot "max-degree-subtotals.tsv" using 1:3:4:5 with yerrorbars lt 1 lc 1 lw 2 title "min-avg-max",
     "" using 1:6 with lines lt 3 lc 3 title "mean",
     "" using 1:7 with lines lt 3 lc 4 title "80%",
     "" using 1:8 with lines lt 3 lc 7 title "90%";
'
