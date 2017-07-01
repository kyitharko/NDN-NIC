#!/usr/bin/gawk -f
# Collect packet bytes and number of BF update commands.
# Usage: ./bfu-one.awk -v PREFIX=nd-prefix < list-of-hosts

BEGIN {
  OFS = "\t"
  totalPkts = 0
  totalPktSize = 0
  totalBfSets = 0
  totalBfClears = 0
  print "host", "nPkts", "pktSize", "nBfSets", "nBfClears"
}
{
  host = $1
  if (host == "") { next }

  nPkts = 0
  pktSize = 0
  nBfSets = 0
  nBfClears = 0

  ndFile = PREFIX "." host ".nd.tsv.xz"
  bfuFile = PREFIX "." host ".bfu.tsv.xz"

  while (("xzcat " ndFile |& getline) > 0) {
    ++nPkts
    pktSize += $4
  }
  close("xzcat " ndFile)

  while (("xzcat " bfuFile |& getline) > 0) {
    nBfSets += $5 + $7 + $9
    nBfClears += $6 + $8 + $10
  }
  close("xzcat " bfuFile)

  print host, nPkts, pktSize, nBfSets, nBfClears
  totalPkts += nPkts
  totalPktSize += pktSize
  totalBfSets += nBfSets
  totalBfClears += nBfClears
}
END {
  print "+", totalPkts, totalPktSize, totalBfSets, totalBfClears
}
