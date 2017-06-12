# NDN-NIC experiment parameters

This branch contains the exact parameters used to generate the plots.

## NFS to TTT

1.  Process NFS trace by the hour with nfsdump `timeofday.sh` script.

2.  Run Mininet experiment with `nfs-exp-hour.sh`.

3.  Collect traffic statistics:

        for DIR in $(bash nfs-hours.sh); do pushd $DIR && ls *.ttt.tsv.xz | $NDNNICROOT/analyze/ttt-stats.awk > ttt-stats.tsv && popd; done

## NIC simulation

1.  Export NDN-NIC path (scripts from NDN-NIC master branch):

        export NDNNICROOT=$HOME/NDN-NIC

2.  Generate polynomial terms used in Bloom filter's hash functions:

        dd if=/dev/urandom of=bf1.poly bs=1M count=64
        dd if=/dev/urandom of=bf2.poly bs=1M count=64
        dd if=/dev/urandom of=bf3.poly bs=1M count=64

3.  Establish baselines:

        for DIR in $(bash nfs-hours.sh); do pushd $DIR && bash $NDNNICROOT/analyze/packet-processing-base.sh && bash $NDNNICROOT/analyze/max-degree.sh && popd; done

4.  Run regular and optimal NIC simulations:

        for DIR in $(bash nfs-hours.sh); do pushd $DIR && bash $NDNNICROOT/analyze/one.sh regular && bash $NDNNICROOT/analyze/one.sh optimal && popd; done

5.  Run bfsize script:

        for DIR in $(bash nfs-hours.sh); do pushd $DIR && bash ../bfsize.sh && popd; done

6.  Run nhash script:

        for DIR in $(bash nfs-hours.sh); do pushd $DIR && bash ../nhash.sh && popd; done

7.  Run active thresholds script:

        for DIR in $(bash nfs-hours.sh); do pushd $DIR && bash ../active.sh && popd; done

## Plotting

See scripts in paper repository.
