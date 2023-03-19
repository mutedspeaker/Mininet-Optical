set -e
url="localhost:8080";
t1=$url; t2=$url; t3=$url; t4=$url; t5=$url; t6=$url; t7=$url; t8=$url; t9=$url; t10=$url; 
r1=$url; r2=$url; r3=$url
curl="curl -s"
$curl "$t1/connect?node=t1&ethPort=3&wdmPort=3&channel=9"
$curl "$t2/connect?node=t2&ethPort=4&wdmPort=4&channel=18"
$curl "$t3/connect?node=t3&ethPort=5&wdmPort=5&channel=27"
$curl "$t4/connect?node=t4&ethPort=6&wdmPort=6&channel=36"
$curl "$t5/connect?node=t5&ethPort=7&wdmPort=7&channel=45"
$curl "$t6/connect?node=t6&ethPort=8&wdmPort=8&channel=54"
$curl "$t7/connect?node=t7&ethPort=9&wdmPort=9&channel=63"
$curl "$t8/connect?node=t8&ethPort=10&wdmPort=10&channel=72"
$curl "$t9/connect?node=t9&ethPort=11&wdmPort=11&channel=81"
$curl "$t10/connect?node=t10&ethPort=12&wdmPort=12&channel=90"
$curl "$r1/reset?node=r1"
$curl "$r2/reset?node=r2"
$curl "$r3/reset?node=r3"
$curl "$r1/connect?node=r1&port1=3&port2=3&channels=9"
$curl "$r1/connect?node=r1&port1=4&port2=4&channels=18"
$curl "$r1/connect?node=r1&port1=5&port2=5&channels=27"
$curl "$r2/connect?node=r2&port1=6&port2=6&channels=36"
$curl "$r2/connect?node=r2&port1=7&port2=7&channels=45"
$curl "$r2/connect?node=r2&port1=8&port2=8&channels=54"
$curl "$r2/connect?node=r2&port1=9&port2=9&channels=63"
$curl "$r3/connect?node=r3&port1=10&port2=10&channels=72"
$curl "$r3/connect?node=r3&port1=11&port2=11&channels=81"
$curl "$r3/connect?node=r3&port1=12&port2=12&channels=90"

$curl "$r1/connect?node=r1&port1=300&port2=300&channels=40"
$curl "$r2/connect?node=r2&port1=310&port2=310&channels=40"
$curl "$r2/connect?node=r2&port1=400&port2=400&channels=50"
$curl "$r3/connect?node=r3&port1=410&port2=410&channels=50"

# turn on the roadm
$curl "$t1/turn_on?node=t1"
$curl "$t2/turn_on?node=t2"
$curl "$t3/turn_on?node=t3"
$curl "$t4/turn_on?node=t4"
$curl "$t5/turn_on?node=t5"
$curl "$t6/turn_on?node=t6"
$curl "$t7/turn_on?node=t7"
$curl "$t8/turn_on?node=t8"
$curl "$t9/turn_on?node=t9"
$curl "$t10/turn_on?node=t10"

for tname in t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 ; do
    url=${!tname}
    $curl "$url/monitor?monitor=$tname-monitor"
done

    
for tname in t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 ; do
    url=${!tname}
    #echo "* $tname"
    $curl "$url/monitor?monitor=$tname-monitor"
done
