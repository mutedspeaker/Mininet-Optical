set -e
url="localhost:8080";
declare -a t=() # declare an array
for ((i=1;i<=n+1;i++)); do
    t[i]=$url
done
r1=$url; r2=$url; r3=$url
curl="curl -s"
echo "* Configuring terminals in threeRoadms.py network"
# loop through the array and call the curl command
for ((i=1;i<=n;i++)); do
    $curl "$url/t${t[i]}/connect?node=t${t[i]}&ethPort=$((i+2))&wdmPort=$((i+2))&channel=$((i*6))"
done
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
# turn on the roadm
    for ((i=1;i<=n;i++)); do
        curl "$url$t[i]/turn_on?node=t$i"
    done

    for ((i=1;i<=n;i++)); do
        tname="t$i"
        url="${t[i]}"
        $curl "$url/monitor?monitor=$tname-monitor"
    done
echo "* Monitoring signals at endpoints"
for ((i=1;i<=n;i++)); do
        tname="t$i"
        url=${t[$i]}
        echo "* $tname"
        $curl "$url/monitor?monitor=$tname-monitor"
    done
echo "* 007 OUT!"
