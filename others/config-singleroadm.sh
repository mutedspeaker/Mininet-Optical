#!/bin/bash -x

set -e  # exit script on error

# URL for REST server
url="localhost:8080"; t1=$url; t2=$url; t3=$url; r1=$url
curl="curl -s"

echo "* Configuring terminals in singleroadm.py network"

$curl "$t1/connect?node=t1&ethPort=1&wdmPort=20&channel=1"
$curl "$t1/connect?node=t1&ethPort=1&wdmPort=30&channel=1"

$curl "$t2/connect?node=t2&ethPort=1&wdmPort=50&channel=2"
$curl "$t2/connect?node=t2&ethPort=1&wdmPort=60&channel=2"

$curl "$t3/connect?node=t3&ethPort=1&wdmPort=70&channel=3"
$curl "$t3/connect?node=t3&ethPort=1&wdmPort=80&channel=3"

echo "* Monitoring signals at endpoints"
for tname in t1 t2 t3; do
    url=${!tname}
    $curl "$url/monitor?monitor=$tname-monitor"
done

echo "* Resetting ROADM"
$curl "$r1/reset?node=r1"

echo "* Configuring ROADM to forward ch1 from t1 to t2"

$curl "$r1/connect?node=r1&port1=20&port2=20&channels=1"
$curl "$r1/connect?node=r1&port1=30&port2=30&channels=1"

$curl "$r1/connect?node=r1&port1=50&port2=50&channels=2"
$curl "$r1/connect?node=r1&port1=60&port2=60&channels=2"

$curl "$r1/connect?node=r1&port1=70&port2=70&channels=3"
$curl "$r1/connect?node=r1&port1=80&port2=80&channels=3"

echo "* Turning on terminals/transceivers"

$curl "$t1/turn_on?node=t1"
$curl "$t2/turn_on?node=t2"
$curl "$t3/turn_on?node=t3"

echo "* Monitoring signals at endpoints"
for tname in t1 t2 t3; do
    url=${!tname}
    echo "* $tname"
    $curl "$url/monitor?monitor=$tname-monitor"
done

echo "* Done."
