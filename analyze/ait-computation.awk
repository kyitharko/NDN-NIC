#!/usr/bin/gawk -f
# Estimation computation overhead from existing AIT trace logs.
# Usage: ls *.ait-trace.log.xz | ait-computation.awk
#
# nNodeAccess field indicates how many NameTree nodes are accessed during an insert/erase operation.
# It is calculated according to children count in updateCs2Fields operation, and de-duplicated if
# updateCs2Fields is called multiple times on the same node during a single insert/erase operation.

BEGIN {
  OFS = "\t"
  totalTransformation = 0
  totalAggregation = 0
  totalReversion = 0
  totalNodeAccess = 0
  print "host", "nTransformation", "nAggregation", "nReversion", "nNodeAccess"
}
{
  file = $1
  if (file == "") { next }
  n = split(file, a, ".")
  host = a[n-3]

  nTransformation = 0
  nAggregation = 0
  nReversion = 0
  nNodeAccess = 0

  while (("xzcat " file |& getline) > 0) {
    if ($1 == "transformation") {
      ++nTransformation
    }
    if ($1 == "aggregation") {
      ++nAggregation
    }
    if ($1 == "reversion" && $4 != "none") {
      ++nReversion
    }

    if ($1 == "insert" || $1 == "erase") {
      delete updateCs2Fields_map
    }
    if ($1 == "updateCs2Fields") {
      nChildren = int(substr($3, 11))
      if (!($2 in updateCs2Fields_map)) {
        updateCs2Fields_map[$2] = 0
      }
      nChildrenIncr = nChildren - updateCs2Fields_map[$2]
      if (nChildrenIncr > 0) {
        nNodeAccess += nChildrenIncr
        updateCs2Fields_map[$2] = nChildren
      }
    }
  }
  close("xzcat " file)

  print host, nTransformation, nAggregation, nReversion, nNodeAccess
  totalTransformation += nTransformation
  totalAggregation += nAggregation
  totalReversion += nReversion
  totalNodeAccess += nNodeAccess
}
END {
  print "+", totalTransformation, totalAggregation, totalReversion, totalNodeAccess
}
