# NDN-NIC experiment parameters

This branch contains the exact parameters used to generate the plots.

## NFS to TTT

1. Process NFS trace by the hour with nfsdump `timeofday.sh` script.
2. Run Mininet experiment with `nfs-exp-hour.sh`.

## NIC simulation

1.  Export NDN-NIC path (scripts from NDN-NIC master branch):

        export NDNNICROOT=$HOME/NDN-NIC

2.  Generate polynomial terms used in Bloom filter's hash functions:

        dd if=/dev/urandom of=bf1.poly bs=1M count=64
        dd if=/dev/urandom of=bf2.poly bs=1M count=64
        dd if=/dev/urandom of=bf3.poly bs=1M count=64

3.  Establish baseline of packet processing overhead:

        for DIR in $(bash nfs-hours.sh); do pushd $DIR && bash $NDNNICROOT/analyze/packet-processing-base.sh && popd; done

4.  Run bfsize script:

        for DIR in $(bash nfs-hours.sh); do pushd $DIR && bash ../bfsize.sh && popd; done

5.  Run nhash script:

        for DIR in $(bash nfs-hours.sh); do pushd $DIR && bash ../nhash.sh && popd; done

## Plotting

See scripts in paper repository.
