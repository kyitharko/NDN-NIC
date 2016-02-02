#!/usr/bin/gawk -f
# Estimation computation overhead from existing AIT trace logs.
# Usage: ls *.ait-trace.log.xz | ait-computation.awk

BEGIN {
  OFS = "\t"

  print "host", "nReduction2", "nReduction1", "nReductionPmfp", "updateCs2Fields_nChildren", "updateCs2Fields_dedup"
}
{
  file = $1
  if (file == "") { next }
  n = split(file, a, ".")
  host = a[n-3]

  nReduction2 = 0
  nReduction1 = 0
  nReductionPmfp = 0
  updateCs2Fields_nChildren = 0
  updateCs2Fields_dedup = 0

  while (("xzcat " file |& getline) > 0) {
    if ($1 == "reduction2") {
      ++nReduction2
    }
    if ($1 == "reduction1") {
      ++nReduction1
    }
    if ($1 == "reductionPmfp" && $4 != "none") {
      ++nReductionPmfp
    }

    if ($1 == "insert" || $1 == "erase") {
      delete updateCs2Fields_map
    }
    if ($1 == "updateCs2Fields") {
      nChildren = int(substr($3, 11))
      updateCs2Fields_nChildren += nChildren
      if ($2 in updateCs2Fields_map) {
        nChildrenIncr = nChildren - updateCs2Fields_map[$2]
      }
      else {
        nChildrenIncr = nChildren
      }
      if (nChildrenIncr > 0) {
        updateCs2Fields_dedup += nChildrenIncr
        updateCs2Fields_map[$2] = nChildren
      }
    }
  }
  close("xzcat " file)

  print host, nReduction2, nReduction1, nReductionPmfp, updateCs2Fields_nChildren, updateCs2Fields_dedup
}
