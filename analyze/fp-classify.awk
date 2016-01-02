#!/usr/bin/gawk -f
# Classify false positive reasons from existing NIC decision logs.
# Usage: fp-classify.awk *.nd.tsv

BEGIN {
  SUBSEP = " "
  FS = OFS = "\t"

  category_BF = 1
  category_PM = 2
  category_PT = 4
  category_MAX = 7

  classify["I","FP1"] = category_BF
  classify["I","FP2"] = category_BF
  classify["D","FP1"] = category_BF
  classify["D","FP2"] = category_BF
  classify["I","CS1"] = category_PM
  classify["D","FIB1"] = category_PT
  classify["I","PIT1"] = category_PT
  classify["D","CS1"] = category_PT
  classify["D","CS2"] = category_PT

  print "FILENAME", "PACKETS", "BF", "PM", "BF+PM", "PT", "BF+PT", "PM+PT", "BF+PM+PT"
}
BEGINFILE {
  nPackets = 0
  for (i=1; i<=category_MAX; ++i) {
    nFps[i] = 0
  }
}
{
  ++nPackets
}
$4=="DROP" && $5!="DROP" {
  nReasons = split($5, reasons, ",")
  category = 0
  for (i=1; i<=nReasons; ++i) {
    category = or(category, classify[$2,reasons[i]])
  }
  ++nFps[category]
}
ENDFILE {
  nPacketsTotal += nPackets
  for (i=1; i<=category_MAX; ++i) {
    nFpsTotal[i] += nFps[i]
  }

  print FILENAME, nPackets, nFps[1], nFps[2], nFps[3], nFps[4], nFps[5], nFps[6], nFps[7]
}
END {
  print "*", nPacketsTotal, nFpsTotal[1], nFpsTotal[2], nFpsTotal[3], nFpsTotal[4], nFpsTotal[5], nFpsTotal[6], nFpsTotal[7]
}
