#!/bin/bash -x

set -e  # exit script on error

# URL for REST server
url="localhost:8080"; t1=$url; t2=$url; t3=$url; t4=$url;  r1=$url; r2=$url; r3=$url

curl="curl -s"

echo "* Configuring terminals in threeRoadms.py network"

$curl "$t1/connect?node=t1&ethPort=1&wdmPort=10&channel=1"
$curl "$t1/connect?node=t1&ethPort=1&wdmPort=11&channel=1"

$curl "$t2/connect?node=t2&ethPort=1&wdmPort=10&channel=40"
$curl "$t2/connect?node=t2&ethPort=1&wdmPort=11&channel=40"

$curl "$t2/connect?node=t2&ethPort=1&wdmPort=20&channel=50"
$curl "$t2/connect?node=t2&ethPort=1&wdmPort=21&channel=50"

$curl "$t3/connect?node=t3&ethPort=1&wdmPort=10&channel=60"
$curl "$t3/connect?node=t3&ethPort=1&wdmPort=11&channel=60"

$curl "$t3/connect?node=t3&ethPort=1&wdmPort=20&channel=70"
$curl "$t3/connect?node=t3&ethPort=1&wdmPort=21&channel=70"

$curl "$t4/connect?node=t3&ethPort=1&wdmPort=10&channel=90"
$curl "$t4/connect?node=t3&ethPort=1&wdmPort=11&channel=90"

echo "* Monitoring signals at endpoints"
for tname in t1 t2 t3 t4; do
    url=${!tname}
    $curl "$url/monitor?monitor=$tname-monitor"
done

echo "* Resetting ROADM"
$curl "$r1/reset?node=r1"
$curl "$r2/reset?node=r2"
$curl "$r3/reset?node=r3"

echo "* Configuring ROADM to forward ch1 from t1 to t2"

$curl "$r1/connect?node=r1&port1=10&port2=10&channels=1"
$curl "$r1/connect?node=r1&port1=11&port2=11&channels=1"

$curl "$r1/connect?node=r1&port1=10&port2=10&channels=40"
$curl "$r1/connect?node=r1&port1=11&port2=11&channels=40"

$curl "$r2/connect?node=r2&port1=20&port2=20&channels=50"
$curl "$r2/connect?node=r2&port1=21&port2=21&channels=50"

$curl "$r2/connect?node=r2&port1=10&port2=10&channels=60"
$curl "$r2/connect?node=r2&port1=11&port2=11&channels=60"

$curl "$r3/connect?node=r3&port1=20&port2=20&channels=70"
$curl "$r3/connect?node=r3&port1=21&port2=21&channels=70"

$curl "$r3/connect?node=r3&port1=10&port2=10&channels=90"
$curl "$r3/connect?node=r3&port1=11&port2=11&channels=90"

echo "* Turning on terminals/transceivers"

$curl "$t1/turn_on?node=t1"
$curl "$t2/turn_on?node=t2"
$curl "$t3/turn_on?node=t3"
$curl "$t4/turn_on?node=t4"

echo "* Monitoring signals at endpoints"
for tname in t1 t2 t3 t4; do
    url=${!tname}
    echo "* $tname"
    $curl "$url/monitor?monitor=$tname-monitor"
done

echo "* Done."
