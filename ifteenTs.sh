#!/bin/bash -x

set -e  # exit script on error

# URL for REST server
url="localhost:8080"; t1=$url; t2=$url; t3=$url;r1=$url; r2=$url; r3=$url

curl="curl -s"

echo "* Configuring terminals in threeRoadms.py network"

$curl "$t1/connect?node=t1&ethPort=3&wdmPort=2&channel=41"
$curl "$t2/connect?node=t2&ethPort=7&wdmPort=7&channel=45"
$curl "$t3/connect?node=t3&ethPort=5&wdmPort=5&channel=49"

echo "* Resetting ROADM"
$curl "$r1/reset?node=r1"
$curl "$r2/reset?node=r2"
$curl "$r3/reset?node=r3"

echo "* Monitoring signals at endpoints"


echo "* Configuring ROADM to forward ch1 from t1 to t2"
# r1 and t1
$curl "$r1/connect?node=r1&port1=2&port2=2&channels=41"

# r1 and r2 ig
$curl "$r1/connect?node=r1&port1=3&port2=3&channels=40"
$curl "$r2/connect?node=r2&port1=30&port2=30&channels=40"
# r2 and r3
$curl "$r2/connect?node=r2&port1=4&port2=4&channels=50"
$curl "$r2/connect?node=r2&port1=40&port2=40&channels=50"
# r2 and t2
$curl "$r2/connect?node=r2&port1=7&port2=7&channels=45"

#r3 and t3
$curl "$r3/connect?node=r3&port1=5&port2=5&channels=49"

echo "* Turning on terminals/transceivers"

$curl "$t1/turn_on?node=t1"
$curl "$t2/turn_on?node=t2"
$curl "$t3/turn_on?node=t3"

for tname in t1 t2 t3; do
    url=${!tname}
    $curl "$url/monitor?monitor=$tname-monitor"
done

echo "* Monitoring signals at endpoints"
for tname in t1 t2 t3; do
    url=${!tname}
    echo "* $tname"
    $curl "$url/monitor?monitor=$tname-monitor"
done


echo "* Done."
