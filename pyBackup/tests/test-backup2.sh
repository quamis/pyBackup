#!/bin/bash

echo "initialize"

SRC="test-data/tmp-data/"
DST="test-data/DST/"

function do_sync {
	echo "----------------- SYNC ----------------"
	echo "calculate local hashes"
	python ./test-Hasher-FastContentHashV1Cached.py --verbose=0 --useCache=0 --data="$SRC" --cache="$SRC/backup.sqlite" 

	#echo "compare"
	#python ./test-Comparer.py --cacheNew="$SRC/backup.sqlite" --cacheOld="$DST/backup.sqlite" --doApply=0

	echo "compare & update changes"
	python ./test-Writer-LocalPathWriter.py --verbose=0 --cacheNew="$SRC/backup.sqlite" --cacheOld="$DST/backup.sqlite" --destination="$DST" --source="$SRC"
}

echo "----------------- initialize ----------------"
# simulate a fist-backup
rm -rf "$SRC"; mkdir "$SRC";
rm -rf "$DST"; mkdir "$DST";

# populate, initial data
#cp -rf "test-data/data-m/" "$SRC"
echo "new file" > "$SRC/new_file_000.txt";
do_sync;
cp -f "$SRC/backup.sqlite" "$DST/backup.sqlite"

echo "delete"
rm -f "$SRC/new_file_000.txt";
do_sync;

