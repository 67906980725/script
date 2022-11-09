
#!/usr/bin/bash

group=$1
cur_path=$(dirname $(readlink -f "$0"))
dir="$cur_path/$group"

for item in `ls $dir`; do
        echo "$item"
	gtk-launch $item
done

