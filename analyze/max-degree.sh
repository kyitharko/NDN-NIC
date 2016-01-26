#!/bin/bash
# Plot max-degree from any ait-trace.
# Usage: ./max-degree.sh

R="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"

KEY=$(ls *.ait-trace.log.xz | awk 'BEGIN { FS=OFS="." } NR==1 { NF-=4; print }')

ls $KEY.*.ait-trace.log.xz | gawk '
BEGIN {
  OFS = "\t"
}
{
  file = $1
  n = split(file, a, ".")
  host = a[n-3]

  while (("xzcat " file |& getline) > 0) {
    if ($1 == "parentDegree") {
      name = $2
      degree = substr($3, 8)
      if (degree > maxDegree[name]) {
        maxDegree[name] = degree
      }
    }
  }

  for (name in maxDegree) {
    nComponents = split(name, a, "/") - 1
    if (name == "/") {
      nComponents = 0
    }
    print host, name, nComponents, maxDegree[name]
  }
  delete maxDegree
}
' > max-degree.tsv

sort -k3n -k4n max-degree.tsv \
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
  nComponents = -1
  sum = cnt = 0
}
$3!=nComponents {
  printSubtotal()

  nComponents = $3
  sum = cnt = 0
  delete vector
}
{
  vector[cnt] = $4
  ++cnt
  sum += $4
}
END {
  printSubtotal()
}
' > max-degree-subtotals.tsv

YMAX=$(cut -f8 max-degree-subtotals.tsv | sort -nr | head -1)
YMAX=$((2*YMAX))

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
