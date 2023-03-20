awk '/^(*** t)[0-9][0-9]?( )/ {print substr($0,5)}' output.txt > final.txt;


