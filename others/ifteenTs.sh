#!/bin/bash -x
set -e  # exit script on error

# URL for REST server
url="localhost:8080"; t1=$url; t2=$url; t3=$url; t4=$url; t5=$url; t6=$url; t7=$url; t8=$url; t9=$url; t10=$url; t11=$url; t12=$url; t13=$url; t14=$url; t15=$url; r1=$url; r2=$url; r3=$url

curl="curl -s"

echo "* Configuring terminals in threeRoadms.py network"
$curl "$t1/connect?node=t1&ethPort=2&wdmPort=3&channel=6"
$curl "$t2/connect?node=t2&ethPort=3&wdmPort=4&channel=12"
$curl "$t3/connect?node=t3&ethPort=4&wdmPort=5&channel=18"
$curl "$t4/connect?node=t4&ethPort=5&wdmPort=6&channel=24"
$curl "$t5/connect?node=t5&ethPort=1&wdmPort=7&channel=30"
$curl "$t6/connect?node=t6&ethPort=2&wdmPort=8&channel=36"
$curl "$t7/connect?node=t7&ethPort=3&wdmPort=9&channel=42"
$curl "$t8/connect?node=t8&ethPort=4&wdmPort=10&channel=48"
$curl "$t9/connect?node=t9&ethPort=5&wdmPort=11&channel=54"
$curl "$t10/connect?node=t10&ethPort=1&wdmPort=12&channel=60"
$curl "$t11/connect?node=t11&ethPort=2&wdmPort=13&channel=66"
$curl "$t12/connect?node=t12&ethPort=3&wdmPort=14&channel=72"
$curl "$t13/connect?node=t13&ethPort=4&wdmPort=15&channel=78"
$curl "$t14/connect?node=t14&ethPort=5&wdmPort=16&channel=84"
$curl "$t15/connect?node=t15&ethPort=1&wdmPort=17&channel=90"

echo "* Resetting ROADM"
$curl "$r1/reset?node=r1"
$curl "$r2/reset?node=r2"
$curl "$r3/reset?node=r3"

echo "* Monitoring signals at endpoints"


echo "* Configuring ROADM to forward ch1 from t1 to t2"
$curl "$r1/connect?node=r1&port1=3&port2=3&channels=6"
$curl "$r1/connect?node=r1&port1=4&port2=4&channels=12"
$curl "$r1/connect?node=r1&port1=5&port2=5&channels=18"
$curl "$r1/connect?node=r1&port1=6&port2=6&channels=24"
$curl "$r1/connect?node=r1&port1=7&port2=7&channels=30"
$curl "$r2/connect?node=r2&port1=8&port2=8&channels=36"
$curl "$r2/connect?node=r2&port1=9&port2=9&channels=42"
$curl "$r2/connect?node=r2&port1=10&port2=10&channels=48"
$curl "$r2/connect?node=r2&port1=11&port2=11&channels=54"
$curl "$r2/connect?node=r2&port1=12&port2=12&channels=60"
$curl "$r3/connect?node=r3&port1=13&port2=13&channels=66"
$curl "$r3/connect?node=r3&port1=14&port2=14&channels=72"
$curl "$r3/connect?node=r3&port1=15&port2=15&channels=78"
$curl "$r3/connect?node=r3&port1=16&port2=16&channels=84"
$curl "$r3/connect?node=r3&port1=17&port2=17&channels=90"

# r1 and r2 
$curl "$r1/connect?node=r1&port1=30&port2=30&channels=40"
$curl "$r2/connect?node=r2&port1=31&port2=31&channels=40"
# r2 and r3
$curl "$r2/connect?node=r2&port1=40&port2=40&channels=50"
$curl "$r3/connect?node=r3&port1=41&port2=41&channels=50"
# r2 and t2
echo "* Turning on terminals/transceivers"

$curl "$t1/turn_on?node=t1"
$curl "$t2/turn_on?node=t2"
$curl "$t3/turn_on?node=t3"
$curl "$t3/turn_on?node=t4"
$curl "$t3/turn_on?node=t5"
$curl "$t3/turn_on?node=t6"
$curl "$t3/turn_on?node=t7"
$curl "$t3/turn_on?node=t8"
$curl "$t3/turn_on?node=t9"
$curl "$t3/turn_on?node=t10"
$curl "$t3/turn_on?node=t11"
$curl "$t3/turn_on?node=t12"
$curl "$t3/turn_on?node=t13"
$curl "$t3/turn_on?node=t14"
$curl "$t3/turn_on?node=t15"

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
