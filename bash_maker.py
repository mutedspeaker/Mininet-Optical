def bash_text():
    
    a = ''
    a += "set -e\n"
    a += 'url="localhost:8080";\n'
    a += 't1=$url; t2=$url; t3=$url; t4=$url; t5=$url; t6=$url;\n'
    a += 't7=$url; t8=$url; t9=$url; t10=$url; t11=$url; t12=$url; t13=$url; t14=$url; t15=$url; r1=$url; r2=$url; r3=$url\n'
    a += 'curl="curl -s"\n'
    a += 'echo "* Configuring terminals in threeRoadms.py network"\n'

    for i in range(1,16):
        a += f'$curl "$t{i}/connect?node=t{i}&ethPort={i+2}&wdmPort={i+2}&channel={i*6}"\n'

    a += 'echo "* Resetting ROADM"\n'

    for i in range(1,4):
        a += f'$curl "$r{i}/reset?node=r{i}"\n'

    a += 'echo "* Configuring ROADM to forward ch1 from t1 to t2"\n'

    for i in range(1,6):
        a += f'$curl "$r1/connect?node=r1&port1={i+2}&port2={i+2}&channels={i*6}"\n'
    for i in range(6,11):
        a += f'$curl "$r2/connect?node=r2&port1={i+2}&port2={i+2}&channels={i*6}"\n'
    for i in range(11,16):
        a += f'$curl "$r3/connect?node=r3&port1={i+2}&port2={i+2}&channels={i*6}"\n'

    a += '$curl "$r1/connect?node=r1&port1=30&port2=30&channels=40"\n'
    a += '$curl "$r2/connect?node=r2&port1=31&port2=31&channels=40"\n'
    a += '$curl "$r2/connect?node=r2&port1=40&port2=40&channels=50"\n'
    a += '$curl "$r3/connect?node=r3&port1=41&port2=41&channels=50"\n'

    for i in range(1, 16):
        a += f'$curl "$t{i}/turn_on?node=t{i}"\n'

    a += 'for tname in t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12 t13 t14 t15; do\n'
    a += '    url=${!tname}\n'
    a += '    $curl "$url/monitor?monitor=$tname-monitor"\n'
    a += 'done\n'
    a += 'echo "* Monitoring signals at endpoints"\n'
    a += 'for tname in t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12 t13 t14 t15; do\n'
    a += '    url=${!tname}\n'
    a += '    echo "* $tname"\n'
    a += '    $curl "$url/monitor?monitor=$tname-monitor"\n'
    a += 'done\n'

    a += 'echo "* 007 OUT!"\n'
    
    return a
def bash_creator(a):
    f= open("bash1.sh","w+")
    f.write(a)
    f.close()
a = bash_text()
bash_creator(a)
