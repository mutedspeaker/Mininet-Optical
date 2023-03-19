# regex_part = '\*\*\* t'
# awk '/^(*** t)[1-9][1-9]?( )/  {print substr($0,5)}'  output.txt
#!/bin/bash

while read line; do
  if [[ $line == "*** t"* ]]; then
    t=$(echo "$line" | awk '{print $1}' | cut -c 4-)
    ch=$(echo "$line" | awk '{print $2}' | cut -c 3-)
    freq=$(echo "$line" | awk '{print $3}' | cut -c 2- | sed 's/THz//')
    gosnr=$(echo "$line" | awk '{print $9}')
    osnr=$(echo "$line" | awk '{print $11}')
    echo "$t $ch $freq $gosnr $osnr"
  fi
done < output.txt

