#!/bin/bash

echo "initialize"

#SRC="/media/BIG/books/raw/Romanian.Book.Colection-J4K/"
#SRC="/cygdrive/d/exports/2014-11-21 - adodb logging/"

#DST="test-data/DST/"

#SRC="/media/BIG/music/= testing =/= Andra =/"; DST="/media/lucian/Backup/backups from 2016-09-21/music/= testing =/= Andra =/"
SRC="/cygdrive/d/musiq/dnb - bse podcasts/"; DST="test-data/DST/"

# simulate a fist-backup
#rm -f "$SRC/backup.sqlite"; rm -f "$DST/backup.sqlite";
# test whole-copies, for empty backup DST's
#rm -rf "$DST/"; mkdir "$DST";

echo "calculate local hashes"
python ./test-Hasher-FastContentHashV1Cached.py --verbose=0 --useCache=0 --data="$SRC" --cache="$SRC/backup.sqlite" 

#echo "compare"
#python ./test-Comparer.py --cacheNew="$SRC/backup.sqlite" --cacheOld="$DST/backup.sqlite" --doApply=0


echo "compare & update changes"
python ./test-Writer-LocalPathWriter.py --cacheNew="$SRC/backup.sqlite" --cacheOld="$DST/backup.sqlite" --destination="$DST" --source="$SRC"

#cp -f "$SRC/backup.sqlite" "$DST/backup.sqlite"

echo "update full hashes"
python ./test-BackupHashUpdater.py --cache="$SRC/backup.sqlite" --data="$SRC" --percent=1 --min=5

echo "analize cache"
python ./test-BackupAnalyzer.py --cache="$SRC/backup.sqlite" --data="$SRC"


cp -f "$SRC/backup.sqlite" "$DST/backup.sqlite"
