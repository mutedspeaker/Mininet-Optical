# regex_part = '\*\*\* t'

sed -i'.bak' -e '/^.\{0,2\}t/d' output.txt

