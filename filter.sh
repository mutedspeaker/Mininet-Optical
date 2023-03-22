awk '/^(*** t)[0-9][0-9]?( )/ {print substr($0,5)}' output.txt > final.txt;
rm output.txt
sudo rm bash.sh
sudo rm gConfignRoadms.png
python3 zilter.py
rm final.txt
