set -e
url="localhost:8080";
t1=$url;t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
t{i}=$url;
r1=$url; r2=$url; r3=$url
curl="curl -s"
echo "* Configuring terminals in threeRoadms.py network"
$curl "$t1/connect?node=t1&ethPort=3&wdmPort=3&channel=6"
$curl "$t2/connect?node=t2&ethPort=4&wdmPort=4&channel=12"
$curl "$t3/connect?node=t3&ethPort=5&wdmPort=5&channel=18"
$curl "$t4/connect?node=t4&ethPort=6&wdmPort=6&channel=24"
$curl "$t5/connect?node=t5&ethPort=7&wdmPort=7&channel=30"
$curl "$t6/connect?node=t6&ethPort=8&wdmPort=8&channel=36"
$curl "$t7/connect?node=t7&ethPort=9&wdmPort=9&channel=42"
$curl "$t8/connect?node=t8&ethPort=10&wdmPort=10&channel=48"
$curl "$t9/connect?node=t9&ethPort=11&wdmPort=11&channel=54"
$curl "$t10/connect?node=t10&ethPort=12&wdmPort=12&channel=60"
$curl "$t11/connect?node=t11&ethPort=13&wdmPort=13&channel=66"
$curl "$t12/connect?node=t12&ethPort=14&wdmPort=14&channel=72"
$curl "$t13/connect?node=t13&ethPort=15&wdmPort=15&channel=78"
$curl "$t14/connect?node=t14&ethPort=16&wdmPort=16&channel=84"
$curl "$t15/connect?node=t15&ethPort=17&wdmPort=17&channel=90"
$curl "$t16/connect?node=t16&ethPort=18&wdmPort=18&channel=96"
$curl "$t17/connect?node=t17&ethPort=19&wdmPort=19&channel=102"
$curl "$t18/connect?node=t18&ethPort=20&wdmPort=20&channel=108"
$curl "$t19/connect?node=t19&ethPort=21&wdmPort=21&channel=114"
$curl "$t20/connect?node=t20&ethPort=22&wdmPort=22&channel=120"
$curl "$t21/connect?node=t21&ethPort=23&wdmPort=23&channel=126"
$curl "$t22/connect?node=t22&ethPort=24&wdmPort=24&channel=132"
$curl "$t23/connect?node=t23&ethPort=25&wdmPort=25&channel=138"
$curl "$t24/connect?node=t24&ethPort=26&wdmPort=26&channel=144"
$curl "$t25/connect?node=t25&ethPort=27&wdmPort=27&channel=150"
$curl "$t26/connect?node=t26&ethPort=28&wdmPort=28&channel=156"
$curl "$t27/connect?node=t27&ethPort=29&wdmPort=29&channel=162"
$curl "$t28/connect?node=t28&ethPort=30&wdmPort=30&channel=168"
$curl "$t29/connect?node=t29&ethPort=31&wdmPort=31&channel=174"
$curl "$t30/connect?node=t30&ethPort=32&wdmPort=32&channel=180"
$curl "$t31/connect?node=t31&ethPort=33&wdmPort=33&channel=186"
$curl "$t32/connect?node=t32&ethPort=34&wdmPort=34&channel=192"
$curl "$t33/connect?node=t33&ethPort=35&wdmPort=35&channel=198"
$curl "$t34/connect?node=t34&ethPort=36&wdmPort=36&channel=204"
$curl "$t35/connect?node=t35&ethPort=37&wdmPort=37&channel=210"
$curl "$t36/connect?node=t36&ethPort=38&wdmPort=38&channel=216"
$curl "$t37/connect?node=t37&ethPort=39&wdmPort=39&channel=222"
$curl "$t38/connect?node=t38&ethPort=40&wdmPort=40&channel=228"
$curl "$t39/connect?node=t39&ethPort=41&wdmPort=41&channel=234"
$curl "$t40/connect?node=t40&ethPort=42&wdmPort=42&channel=240"
echo "* Resetting ROADM"
$curl "$r1/reset?node=r1"
$curl "$r2/reset?node=r2"
$curl "$r3/reset?node=r3"
echo "* Configuring ROADM to forward ch1 from t1 to t2"
$curl "$r1/connect?node=r1&port1=3&port2=3&channels=6"
$curl "$r1/connect?node=r1&port1=4&port2=4&channels=12"
$curl "$r1/connect?node=r1&port1=5&port2=5&channels=18"
$curl "$r1/connect?node=r1&port1=6&port2=6&channels=24"
$curl "$r1/connect?node=r1&port1=7&port2=7&channels=30"
$curl "$r1/connect?node=r1&port1=8&port2=8&channels=36"
$curl "$r1/connect?node=r1&port1=9&port2=9&channels=42"
$curl "$r1/connect?node=r1&port1=10&port2=10&channels=48"
$curl "$r1/connect?node=r1&port1=11&port2=11&channels=54"
$curl "$r1/connect?node=r1&port1=12&port2=12&channels=60"
$curl "$r1/connect?node=r1&port1=13&port2=13&channels=66"
$curl "$r1/connect?node=r1&port1=14&port2=14&channels=72"
$curl "$r1/connect?node=r1&port1=15&port2=15&channels=78"
$curl "$r1/connect?node=r1&port1=16&port2=16&channels=84"
$curl "$r2/connect?node=r2&port1=17&port2=17&channels=90"
$curl "$r2/connect?node=r2&port1=19&port2=19&channels=102"
$curl "$r2/connect?node=r2&port1=21&port2=21&channels=114"
$curl "$r2/connect?node=r2&port1=23&port2=23&channels=126"
$curl "$r2/connect?node=r2&port1=25&port2=25&channels=138"
$curl "$r3/connect?node=r3&port1=27&port2=27&channels=150"
$curl "$r3/connect?node=r3&port1=28&port2=28&channels=156"
$curl "$r3/connect?node=r3&port1=29&port2=29&channels=162"
$curl "$r3/connect?node=r3&port1=30&port2=30&channels=168"
$curl "$r3/connect?node=r3&port1=31&port2=31&channels=174"
$curl "$r3/connect?node=r3&port1=32&port2=32&channels=180"
$curl "$r3/connect?node=r3&port1=33&port2=33&channels=186"
$curl "$r3/connect?node=r3&port1=34&port2=34&channels=192"
$curl "$r3/connect?node=r3&port1=35&port2=35&channels=198"
$curl "$r3/connect?node=r3&port1=36&port2=36&channels=204"
$curl "$r3/connect?node=r3&port1=37&port2=37&channels=210"
$curl "$r3/connect?node=r3&port1=38&port2=38&channels=216"
$curl "$r3/connect?node=r3&port1=39&port2=39&channels=222"
$curl "$r3/connect?node=r3&port1=40&port2=40&channels=228"
$curl "$r3/connect?node=r3&port1=41&port2=41&channels=234"
$curl "$r1/connect?node=r1&port1=300&port2=300&channels=40"
$curl "$r2/connect?node=r2&port1=310&port2=310&channels=40"
$curl "$r2/connect?node=r2&port1=400&port2=400&channels=50"
$curl "$r3/connect?node=r3&port1=410&port2=410&channels=50"
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
$curl "$t11/turn_on?node=t11"
$curl "$t12/turn_on?node=t12"
$curl "$t13/turn_on?node=t13"
$curl "$t14/turn_on?node=t14"
$curl "$t15/turn_on?node=t15"
$curl "$t16/turn_on?node=t16"
$curl "$t17/turn_on?node=t17"
$curl "$t18/turn_on?node=t18"
$curl "$t19/turn_on?node=t19"
$curl "$t20/turn_on?node=t20"
$curl "$t21/turn_on?node=t21"
$curl "$t22/turn_on?node=t22"
$curl "$t23/turn_on?node=t23"
$curl "$t24/turn_on?node=t24"
$curl "$t25/turn_on?node=t25"
$curl "$t26/turn_on?node=t26"
$curl "$t27/turn_on?node=t27"
$curl "$t28/turn_on?node=t28"
$curl "$t29/turn_on?node=t29"
$curl "$t30/turn_on?node=t30"
$curl "$t31/turn_on?node=t31"
$curl "$t32/turn_on?node=t32"
$curl "$t33/turn_on?node=t33"
$curl "$t34/turn_on?node=t34"
$curl "$t35/turn_on?node=t35"
$curl "$t36/turn_on?node=t36"
$curl "$t37/turn_on?node=t37"
$curl "$t38/turn_on?node=t38"
$curl "$t39/turn_on?node=t39"
for tname in t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12 t13 t14 t15 t16 t17 t18 t19 t20 t21 t22 t23 t24 t25 t26 t27 t28 t29 t30 t31 t32 t33 t34 t35 t36 t37 t38 t39 t40 ; do
    url=${!tname}
    $curl "$url/monitor?monitor=$tname-monitor"
done
echo "* Monitoring signals at endpoints"
for tname in t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12 t13 t14 t15 t16 t17 t18 t19 t20 t21 t22 t23 t24 t25 t26 t27 t28 t29 t30 t31 t32 t33 t34 t35 t36 t37 t38 t39 t40 ; do
    url=${!tname}
    echo "* $tname"
    $curl "$url/monitor?monitor=$tname-monitor"
done
echo "* 007 OUT!"
