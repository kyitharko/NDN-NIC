#!/usr/bin/gawk -f
# Generate NIC Decision Log for regular or optimal NIC.
# Usage: xzcat x.ttt.tsv.xz | ./special-nic.awk -v kind=[regular|optimal] | xz > x.nd.tsv.xz

BEGIN {
  OFS = "\t"
}
kind=="regular" && $2=="PKT" {
  print $1, $3, $4, $5, $6, "ACCEPT"
}
kind=="optimal" && $2=="PKT" {
  print $1, $3, $4, $5, $6, $6
}
