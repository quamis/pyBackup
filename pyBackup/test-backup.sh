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
	python ./test-Writer-LocalPathWriter.py --verbose=3 --cacheNew="$SRC/backup.sqlite" --cacheOld="$DST/backup.sqlite" --destination="$DST" --source="$SRC"

	
	#echo "update full hashes"
	#python ./test-BackupHashUpdater.py --cache="$SRC/backup.sqlite" --data="$SRC" --percent=0.1 --min=10

	#echo "analize cache"
	#python ./test-BackupAnalyzer.py --cache="$SRC/backup.sqlite" --data="$SRC"
	
	
	#echo "cleanup cache"
	#python ./test-Cache-cleanup.py --cache="$SRC/backup.sqlite" --optimize=1 --removeOldLeafs=1
	
	cp -f "$SRC/backup.sqlite" "$DST/backup.sqlite"
	sleep 1
}

echo "----------------- initialize ----------------"
# simulate a fist-backup
rm -rf "$SRC"; mkdir "$SRC";
rm -rf "$DST"; mkdir "$DST";

# populate, initial data
cp -rf "test-data/data-m/." "$SRC"
do_sync;


echo "copy"
echo "new file" > "$SRC/new_file_001.txt";
do_sync;


echo "duplicate"
cp -f "$SRC/new_file_001.txt" "$SRC/new_file_002.txt";
do_sync;


echo "move"
mv "$SRC/new_file_001.txt" "$SRC/new_file_001m.txt";
do_sync;

echo "delete"
rm -f "$SRC/new_file_001m.txt";
do_sync;

