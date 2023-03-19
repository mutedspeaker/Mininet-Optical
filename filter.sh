awk '/^(*** t)[1-9][1-9]?( )/ {print substr($0,5)}' output.txt > final.txt
awk '/^t[0-9]+ receiving/ {match($0, /<ch([1-9][0-9]?):([0-9]+.[0-9]+)THz>/, arr); printf "%s ch%s %s gOSNR: %s dB OSNR: %s dB\n", $1, arr[1], arr[2], $(NF-1), $NF}' final.txt > final2.txt


