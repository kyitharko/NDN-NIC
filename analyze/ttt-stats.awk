#!/usr/bin/gawk -f
# Produce statistics of TTT.
# Usage: ls *.ttt.tsv.xz | traffic-stats.awk

function max(a, b) {
  return a > b ? a : b;
}
BEGIN {
  OFS = "\t"
  totalHosts = 0
  totalPkts = 0
  totalTableChanges = 0
  maxFib = 0
  maxPit = 0
  maxCs = 0
  print "host", "nPkts", "nAccepts", "nTableChanges", "maxFib", "maxPit", "maxCs"
}
{
  file = $1
  if (file == "") { next }
  n = split(file, a, ".")
  host = a[1]

  nPkts = 0
  nAccepts = 0
  nTableChanges = 0
  delete tableCounts

  while (("xzcat " file |& getline) > 0) {
    if ($2 == "PKT") {
      ++nPkts
      if ($6 != "DROP") {
        ++nAccepts
      }
    }
    else if ($2 == "INS") {
      ++nTableChanges
      ++tableCounts["cur" $3]
      tableCounts["max" $3] = max(tableCounts["max" $3], tableCounts["cur" $3])
    }
    else if ($2 == "DEL") {
      ++nTableChanges
      --tableCounts["cur" $3]
    }
  }
  close("xzcat " file)

  print host, nPkts, nAccepts, nTableChanges, 0+tableCounts["maxFIB"], 0+tableCounts["maxPIT"], 0+tableCounts["maxCS"]
  ++totalHosts
  totalPkts += nPkts
  totalAccepts += nAccepts
  totalTableChanges += nTableChanges
  maxFib = max(maxFib, 0+tableCounts["maxFIB"])
  maxPit = max(maxPit, 0+tableCounts["maxPIT"])
  maxCs = max(maxCs, 0+tableCounts["maxCS"])
}
END {
  print "+" totalHosts, totalPkts, totalAccepts, totalTableChanges, maxFib, maxPit, maxCs
}
