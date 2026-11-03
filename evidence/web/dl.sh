#!/bin/bash
# usage: dl.sh filename url description
cd C:/Users/email/AppData/Local/Temp/ceb/evid/web
curl -sL -A "Mozilla/5.0" -m 90 -o "$1" "$2"
h=$(sha256sum "$1" | cut -d' ' -f1)
printf "%s\t%s\t%s\t%s\t%s\n" "$1" "$2" "$(TZ=MST7 date '+%Y-%m-%d %H:%M MST')" "$h" "$3" >> MANIFEST.tsv
ls -l "$1"; echo $h
