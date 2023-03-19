# regex_part = '\*\*\* t'
awk '/^(*** t)[1-9][1-9]?( )/  {print substr($0,5)}'  output.txt

