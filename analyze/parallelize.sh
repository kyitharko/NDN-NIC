#!/bin/bash
# Run commands in parallel.
# Usage: JOBS=8 ./parallelize.sh < commands.lst
#   JOBS: number of subprocesses
#     If omitted, use number of CPUs.
#     If specified as AxB, A subprocesses are running in parallel,
#     and JOBS environ passed to subprocesses is B.
#   stdin: list of commands

JOBS=${JOBS:-$(grep -c ^processor /proc/cpuinfo)}
JOBS1=$(echo $JOBS | cut -dx -f1)
JOBS2=$(echo $JOBS | cut -dx -sf2-)
JOBS2=${JOBS2:-1}

if [[ $JOBS1 -le 1 ]]; then
  JOBS=$JOBS2
  cat /dev/stdin | bash
  exit
fi

while read -r CMD; do
  while [[ $(jobs -p | wc -l) -ge $JOBS1 ]]; do
    sleep 0.1
  done
  if [[ -n $PARALLEL_VERBOSE ]]; then
    echo "$CMD" >/dev/stderr
  fi
  JOBS=$JOBS2 bash -c "$CMD" &
done
wait
