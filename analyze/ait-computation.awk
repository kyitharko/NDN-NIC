#!/usr/bin/gawk -f
# Estimation computation overhead from existing AIT trace logs.
# Usage: ait-computation.awk *.ait-trace.log

BEGIN {
  OFS = "\t"

  print "host", "nReduction2", "nReduction1", "nReductionPmfp", "updateCs2Fields_nChildren"
}
BEGINFILE {
  nReduction2 = 0
  nReduction1 = 0
  nReductionPmfp = 0
  updateCs2Fields_nChildren = 0
}
$1 == "reduction2" {
  ++nReduction2
}
$1 == "reduction1" {
  ++nReduction1
}
$1 == "reductionPmfp" && $4 != "none" {
  ++nReductionPmfp
}
$1 == "updateCs2Fields" {
  updateCs2Fields_nChildren += int(substr($3, 11))
}
ENDFILE {
  n = split(FILENAME, a, ".")
  host = a[n-2]

  print host, nReduction2, nReduction1, nReductionPmfp, updateCs2Fields_nChildren
}
