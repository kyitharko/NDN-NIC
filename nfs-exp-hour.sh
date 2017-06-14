#!/bin/bash
# Run NFS experiment in Mininet for one-hour trace.
# This should be executed in a virtual machine.
#   /data mounts this repository, read-write.
#   /nfs-dataset mounts the NFS dataset, read-only.
# Usage: /data/nfs-exp-hour.sh <hour>

HOUR=$1
NEXTHOUR=$(printf %02d $((HOUR+1)))
HOUR=$(printf %02d $HOUR)

export NFS_DATASET=/nfs-dataset
export NFS_TIMEPERIOD=${HOUR}00-${NEXTHOUR}00
export NFS_DURATION=3700
export NFS_MIN=200
export NFS_MAX=2000
export PYTHONPATH=$HOME/mnndn
CSCAPACITY=65536

mkdir -p /data/nfs-$NFS_TIMEPERIOD

sudo rm -rf /tmp/mnndn /tmp/nfs-traffic.txt
cd $HOME/NDN-NIC/traffic
./nfs.sh --cs=$CSCAPACITY &> /data/nfs-$NFS_TIMEPERIOD/exp.log

for H in $(ls /tmp/mnndn); do
  cat /tmp/mnndn/$H/var/log/ndn/ttt.tsv.xz >/data/nfs-$NFS_TIMEPERIOD/$H.ttt.tsv.xz
done
cat /tmp/nfs-traffic.txt >/data/nfs-$NFS_TIMEPERIOD/nfs-traffic.txt
