import subprocess

# URL for REST server
def run():
    url = "localhost:8080"
    t = [url]*15
    r = [url]*3

    curl = "curl -s"

    print("* Configuring terminals in threeRoadms.py network")
    # t1
    subprocess.run([curl, f"{t[0]}/connect?node=t1&ethPort=2&wdmPort=3&channel=6"], check=True)
    # t2
    subprocess.run([curl, f"{t[1]}/connect?node=t2&ethPort=3&wdmPort=4&channel=12"], check=True)
    # t3
    subprocess.run([curl, f"{t[2]}/connect?node=t3&ethPort=4&wdmPort=5&channel=18"], check=True)
    # t4
    subprocess.run([curl, f"{t[3]}/connect?node=t4&ethPort=5&wdmPort=6&channel=24"], check=True)
    # t5
    subprocess.run([curl, f"{t[4]}/connect?node=t5&ethPort=1&wdmPort=7&channel=30"], check=True)
    # t6
    subprocess.run([curl, f"{t[5]}/connect?node=t6&ethPort=2&wdmPort=8&channel=36"], check=True)
    # t7
    subprocess.run([curl, f"{t[6]}/connect?node=t7&ethPort=3&wdmPort=9&channel=42"], check=True)
    # t8
    subprocess.run([curl, f"{t[7]}/connect?node=t8&ethPort=4&wdmPort=10&channel=48"], check=True)
    # t9
    subprocess.run([curl, f"{t[8]}/connect?node=t9&ethPort=5&wdmPort=11&channel=54"], check=True)
    # t10
    subprocess.run([curl, f"{t[9]}/connect?node=t10&ethPort=1&wdmPort=12&channel=60"], check=True)
    # t11
    subprocess.run([curl, f"{t[10]}/connect?node=t11&ethPort=2&wdmPort=13&channel=66"], check=True)
    # t12
    subprocess.run([curl, f"{t[11]}/connect?node=t12&ethPort=3&wdmPort=14&channel=72"], check=True)
    # t13
    subprocess.run([curl, f"{t[12]}/connect?node=t13&ethPort=4&wdmPort=15&channel=78"], check=True)
    # t14
    subprocess.run([curl, f"{t[13]}/connect?node=t14&ethPort=5&wdmPort=16&channel=84"], check=True)
    # t15
    subprocess.run([curl, f"{t[14]}/connect?node=t15&ethPort=1&wdmPort=17&channel=90"], check=True)

    print("* Resetting ROADM")
    subprocess.run([curl, f"{r[0]}/reset?node=r1"], check=True)
    subprocess.run([curl, f"{r[1]}/reset?node=r2"], check=True)
    subprocess.run([curl, f"{r[2]}/reset?node=r3"], check=True)

    print("* Monitoring signals at endpoints")

    print("* Configuring ROADM to forward ch1 from t1 to t2")
    for i, port in enumerate(range(3, 8)):
        subprocess.run([curl, f"{r[0]}/connect?node=r1&port1={port}&port2={port}&channels={i*6+6}"], check=True)
    for i, port in enumerate(range(8, 13)):
        subprocess.run([curl, f"{r[1]}/connect?node=r2&port1={port}&port2={port}&channels={i*6+36}"], check=True)
    for i, port in enumerate(range(13, 18)):
        subprocess.run([curl, f"{r[2]}/connect?node=r3&port1={port}&port2={port}&channels={i*6+66}"], check=True)

    # r1 and r2 
    subprocess.run([curl, f"{r[0]}/connect?node=r1&port1=30&port2=30&channels=40"], check=True)
    subprocess.run([curl, f"{r[1]}/connect?node=r2&port1=31&port2=31&channels=40"], check=True)

    # r2 and r3 
    subprocess.run([curl, f"{r[1]}/connect?node=r2&port1=40&port2=40&channels=50"], check=True)
    subprocess.run([curl, f"{r[2]}/connect?node=r3&port1=41&port2=41&channels=50"], check=True)

    t = [f"{url}/turn_on?node=t{i}" for i in range(1, 16)]
    for i in range(15):
        subprocess.run(['curl', t[i]], check=True)

    print("* Monitoring signals at endpoints")
    for i in range(1, 16):
        tname = f"t{i}"
        url = t[i-1]
        subprocess.run([curl, f"{url}/monitor?monitor={tname}-monitor"], check=True)
        print(f"* {tname}")  # Moved the print statement inside the loop
    subprocess.run([curl, f"{url}/monitor?monitor={tname}-monitor"], check=True)  # Removed duplicate line

    print("* Done.")
