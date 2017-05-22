#!/bin/bash
# Print folder names for each hour of NFS experiment.
# Usage: for DIR in `bash nfs-hours.sh`; do pushd $DIR && <command> && popd; done
for H in $(seq 0 23); do
  HOUR=$(printf %02d $H)
  NEXTHOUR=$(printf %02d $((H+1)))
  echo nfs-${HOUR}00-${NEXTHOUR}00
done
