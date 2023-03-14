#!/bin/bash -x

set -e  # exit script on error

# URL for REST server
url="localhost:8080"; t1=$url; t2=$url; t3=$url; t4=$url; t5=$url; t6=$url; t7=$url; t8=$url; t9=$url; t10=$url; t11=$url; t12=$url; t13=$url; t14=$url; t15=$url; r1=$url; r2=$url; r3=$url

curl="curl -s"

echo "* Configuring terminals in threeRoadms.py network"
$curl "$t1/connect?node=t1&ethPort=3&wdmPort=2&channel=41"
$curl "$t2/connect?node=t2&ethPort=7&wdmPort=7&channel=45"
$curl "$t3/connect?node=t3&ethPort=5&wdmPort=5&channel=49"
$curl "$t4/connect?node=t4&ethPort=8&wdmPort=8&channel=50"
$curl "$t5/connect?node=t5&ethPort=2&wdmPort=3&channel=42"
$curl "$t6/connect?node=t6&ethPort=1&wdmPort=10&channel=51"
$curl "$t7/connect?node=t7&ethPort=4&wdmPort=11&channel=52"
$curl "$t8/connect?node=t8&ethPort=6&wdmPort=12&channel=53"
$curl "$t9/connect?node=t9&ethPort=7&wdmPort=13&channel=54"
$curl "$t10/connect?node=t10&ethPort=8&wdmPort=15&channel=55"
$curl "$t11/connect?node=t11&ethPort=4&wdmPort=16&channel=56"
$curl "$t12/connect?node=t12&ethPort=5&wdmPort=17&channel=57"
$curl "$t13/connect?node=t13&ethPort=6&wdmPort=18&channel=58"
$curl "$t14/connect?node=t14&ethPort=1&wdmPort=19&channel=59"
$curl "$t15/connect?node=t15&ethPort=2&wdmPort=20&channel=60"

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

for tname in t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12 t13 t14 t15; do
    url=${!tname}
    $curl "$url/monitor?monitor=$tname-monitor"
done

echo "* Monitoring signals at endpoints"
for tname in t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12 t13 t14 t15; do
    url=${!tname}
    echo "* $tname"
    $curl "$url/monitor?monitor=$tname-monitor"
done


echo "* Done."
