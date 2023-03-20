awk '/^(*** t)[0-9][0-9]?( )/ {print substr($0,5)}' out.txt > final.txt;


