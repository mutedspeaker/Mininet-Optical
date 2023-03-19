# regex_part = '\*\*\* t'

sed -i'.bak' -e '/^\(\*\*\* \t\)/!d' output.txt

