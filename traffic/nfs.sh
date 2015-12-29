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

NCLIENTS=$(ls $NFS_DATASET/$NFS_TIMEPERIOD.*.replay | wc -l)
NSERVERS=$(ls $NFS_DATASET/*.paths | wc -l)
NHOSTS=$((NCLIENTS+NSERVERS))

if [[ $NCLIENTS -eq 0 ]]; then
  echo 'No client trace is found.'
  exit 1
fi
if [[ $NSERVERS -eq 0 ]]; then
  echo 'No server paths file is found.'
  exit 1
fi

(
  echo -n nfs
  I=0

  for PATHSFILE in $(ls $NFS_DATASET/*.paths); do
    I=$((I+1))
    HOST=h$I
    echo -n ,s:$HOST:$PATHSFILE
  done

  for OPSTRACE in $(ls $NFS_DATASET/$NFS_TIMEPERIOD.*.replay); do
    I=$((I+1))
    HOST=h$I
    echo -n ,c:$HOST:$HOST:$OPSTRACE
  done
) > /tmp/nfs-traffic.txt

sudo PYTHONPATH=$PYTHONPATH ./exp.py --k $NHOSTS --duration $NFS_DURATION --traffic $(cat /tmp/nfs-traffic.txt)
