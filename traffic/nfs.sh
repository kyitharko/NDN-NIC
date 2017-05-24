#!/bin/bash
# Collect TTT with NFS traffic.

if [[ -z $NFS_DATASET ]] || [[ ! -d $NFS_DATASET ]]; then
  echo '$NFS_DATASET is unspecified or does not exist.'
  exit 2
fi

if [[ -z $NFS_TIMEPERIOD ]]; then
  echo '$NFS_TIMEPERIOD is unspecified.'
  exit 2
fi

if [[ $NFS_DURATION -le 0 ]]; then
  echo '$NFS_DURATION is unspecified or negative.'
  exit 2
fi

(
  echo -n nfs
  I=0

  for SERVER in $(cut -d, -f1 $NFS_DATASET/traceinfo.csv); do
    I=$((I+1))
    HOST=h$I
    echo -n ,s:$HOST:$NFS_DATASET/$SERVER/all.paths
  done

  for OPSTRACE in $(ls $NFS_DATASET/replay/$NFS_TIMEPERIOD.*.ops); do
    ACTIVITY=$(wc -l < $OPSTRACE)
    if [[ -n $NFS_MIN ]] && [[ $ACTIVITY -lt $NFS_MIN ]]; then
      continue
    fi
    if [[ -n $NFS_MAX ]] && [[ $ACTIVITY -gt $NFS_MAX ]]; then
      continue
    fi
    I=$((I+1))
    HOST=h$I
    echo -n ,c:$HOST:$HOST:$OPSTRACE
  done
) >/tmp/nfs-traffic.txt

NHOSTS=$(tr ',' '\n' </tmp/nfs-traffic.txt | wc -l)

sudo PYTHONPATH=$PYTHONPATH ./exp.py --k $NHOSTS --duration $NFS_DURATION --traffic $(cat /tmp/nfs-traffic.txt) "$@"
