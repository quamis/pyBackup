#!/bin/bash

echo "initialize"

#SRC="/media/BIG/books/raw/Romanian.Book.Colection-J4K/"
SRC="/cygdrive/d/exports/2014-11-21 - adodb logging/"
DST="test-data/DST/"

rm "$SRC/backup.sqlite"
rm "$DST/backup.sqlite"

echo "calculate local hashes"
python ./test-Hasher-FastContentHashV1Cached.py --verbose=1 --useCache=0 --data="$SRC" --cache="$SRC/backup.sqlite" 


#echo "compare"
#python ./test-Comparer.py --cacheNew="$SRC/backup.sqlite" --cacheOld="$DST/backup.sqlite"


echo "compare & update changes"
python ./test-Writer-LocalPathWriter.py --cacheNew="$SRC/backup.sqlite" --cacheOld="$DST/backup.sqlite" --destination="$DST" --source="$SRC"

cp -f "$SRC/backup.sqlite" "$DST/backup.sqlite"

#echo "update full hashes"
#python ./test-BackupHashUpdater.py --cache="test-data/tmp-cache/FileSystem1.sqlite" --data="$SRC" --percent=0.1 --min=5

#echo "analize cache"
#python ./test-BackupAnalyzer.py --cache="test-data/tmp-cache/FileSystem1.sqlite" --data="$SRC"
