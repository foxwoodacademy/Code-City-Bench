#!/data/data/com.termux/files/usr/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

filename="$1"
if [ ! -f "$filename" ]; then
    echo "File not found: $filename"
    exit 1
fi

# Find the highest version number
highest_version=$(ls "${filename%.*}"_v*.${filename##*.} 2>/dev/null | awk -F'_v|\\.' '{print $2}' | sort -n | tail -1)

if [ -z "$highest_version" ]; then
    new_version=1
else
    new_version=$((highest_version + 1))
fi

new_filename="${filename%.*}_v${new_version}.${filename##*.}"
cp "$filename" "$new_filename"
echo "Tagged $filename as $new_filename"
