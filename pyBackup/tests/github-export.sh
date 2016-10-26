#!/bin/bash 

DST="./"
OUT="tmp.github-export.txt"


curl -u "$GITHUB_USER":"$GITHUB_PASS" -s "https://api.github.com/users/${GITHUB_USER}/repos?per_page=100" | grep ssh_url | egrep -o "git@github.com:[^\"]+" > $OUT

CWD=`pwd`

while read LINE; do
	echo "$LINE"
	PRJDST=`echo "$LINE"  | egrep -o "/(.+).git" | sed "s/.git//" | sed "s/\///"`
	if [ -d "$PRJDST" ]; then
		cd "$DST/$PRJDST"
		git pull
		cd "$CWD"
	else
		git clone "$LINE" "$DST/$PRJDST"
	fi;
done <"$OUT"
rm -f "$OUT"
