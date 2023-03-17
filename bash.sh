set -e
url="localhost:8080";
declare -a t=() # declare an array
for ((i=0;i<n;i++)); do
    t[i]=$url
done
r1=$url; r2=$url; r3=$url
curl="curl -s"
echo "* Configuring terminals in threeRoadms.py network"
# loop through the array and call the curl command
for ((i=0;i<n;i++)); do
    $curl "$t${t[i]}/connect?node=t${t[i]}&ethPort=$((i+3))&wdmPort=$((i+3))&channel=$((i))"
done
echo "* Resetting ROADM"
$curl "$r1/reset?node=r1"
$curl "$r2/reset?node=r2"
$curl "$r3/reset?node=r3"
echo "* Configuring ROADM to forward ch1 from t1 to t2"
$curl "$r1/connect?node=r1&port1=3&port2=3&channels=1"
$curl "$r1/connect?node=r1&port1=4&port2=4&channels=2"
$curl "$r1/connect?node=r1&port1=5&port2=5&channels=3"
$curl "$r1/connect?node=r1&port1=6&port2=6&channels=4"
$curl "$r1/connect?node=r1&port1=7&port2=7&channels=5"
$curl "$r1/connect?node=r1&port1=8&port2=8&channels=6"
$curl "$r1/connect?node=r1&port1=9&port2=9&channels=7"
$curl "$r1/connect?node=r1&port1=10&port2=10&channels=8"
$curl "$r1/connect?node=r1&port1=11&port2=11&channels=9"
$curl "$r1/connect?node=r1&port1=12&port2=12&channels=10"
$curl "$r1/connect?node=r1&port1=13&port2=13&channels=11"
$curl "$r1/connect?node=r1&port1=14&port2=14&channels=12"
$curl "$r1/connect?node=r1&port1=15&port2=15&channels=13"
$curl "$r1/connect?node=r1&port1=16&port2=16&channels=14"
$curl "$r1/connect?node=r1&port1=17&port2=17&channels=15"
$curl "$r1/connect?node=r1&port1=18&port2=18&channels=16"
$curl "$r1/connect?node=r1&port1=19&port2=19&channels=17"
$curl "$r1/connect?node=r1&port1=20&port2=20&channels=18"
$curl "$r2/connect?node=r2&port1=21&port2=21&channels=19"
$curl "$r2/connect?node=r2&port1=22&port2=22&channels=20"
$curl "$r2/connect?node=r2&port1=23&port2=23&channels=21"
$curl "$r2/connect?node=r2&port1=24&port2=24&channels=22"
$curl "$r3/connect?node=r3&port1=25&port2=25&channels=23"
$curl "$r3/connect?node=r3&port1=26&port2=26&channels=24"
$curl "$r3/connect?node=r3&port1=27&port2=27&channels=25"
$curl "$r3/connect?node=r3&port1=28&port2=28&channels=26"
$curl "$r3/connect?node=r3&port1=29&port2=29&channels=27"
$curl "$r3/connect?node=r3&port1=30&port2=30&channels=28"
$curl "$r3/connect?node=r3&port1=31&port2=31&channels=29"
$curl "$r3/connect?node=r3&port1=32&port2=32&channels=30"
$curl "$r3/connect?node=r3&port1=33&port2=33&channels=31"
$curl "$r3/connect?node=r3&port1=34&port2=34&channels=32"
$curl "$r3/connect?node=r3&port1=35&port2=35&channels=33"
$curl "$r3/connect?node=r3&port1=36&port2=36&channels=34"
$curl "$r3/connect?node=r3&port1=37&port2=37&channels=35"
$curl "$r3/connect?node=r3&port1=38&port2=38&channels=36"
$curl "$r3/connect?node=r3&port1=39&port2=39&channels=37"
$curl "$r3/connect?node=r3&port1=40&port2=40&channels=38"
$curl "$r3/connect?node=r3&port1=41&port2=41&channels=39"
$curl "$r3/connect?node=r3&port1=42&port2=42&channels=40"
$curl "$r1/connect?node=r1&port1=300&port2=300&channels=40"
$curl "$r2/connect?node=r2&port1=310&port2=310&channels=40"
$curl "$r2/connect?node=r2&port1=400&port2=400&channels=50"
$curl "$r3/connect?node=r3&port1=410&port2=410&channels=50"
# turn on the roadm
for ((i=0;i<n;i++)); do
    curl "$t[i]/turn_on?node=t$i"
done
# Monitoring signals before endpoints
for ((i=0;i<n;i++)); do
    tname="t$i"
    url="${t[i]}"
    $curl "$url/monitor?monitor=$tname-monitor"
done
for ((i=0;i<n;i++)); do
    tname="t$i"
    url=${t[$i]}
    echo "* $tname"
    $curl "$url/monitor?monitor=$tname-monitor"
done
echo "* 007 OUT!"
