#!/bin/bash

#This function is used to cleanly exit any script. It does this displaying a
# given error message, and exiting with an error code.
function error_exit {
    echo "$1" >&2   ## Send message to stderr. Exclude >&2 if you don't want it that way.
    exit "${2:-1}"  ## Return a code specified by $2 or 1 by default.
}

#Trap the killer signals so that we can exit with a good message.
trap "error_exit 'Received signal SIGHUP'" SIGHUP
trap "error_exit 'Received signal SIGINT'" SIGINT
trap "error_exit 'Received signal SIGTERM'" SIGTERM


#echo "initialize"

ARR=()
ARR+=(('foo' 'foo'))
for i in ${ARR[@]}; do
    echo "$i"
done

exit

SRC="/media/BIG/books/raw/IT/"; DST="test-data/DST/"; DSTBK="test-data/tmp-data/";
#SRC="/cygdrive/d/exports/2014-11-21 - adodb logging/"


#SRC="/home/lucian/projects/"; DST="/media/lucian/Backup/backups from 2016-09-21/projects/"; DSTBK="/media/lucian/Backup/backups from 2016-09-21/projects.bak/";
#SRC="/media/BIG/music/"; DST="/media/lucian/Backup/backups from 2016-09-21/music/"; DSTBK="/media/lucian/Backup/backups from 2016-09-21/music.bak/";
#SRC="/media/BIG/books/"; DST="/media/lucian/Backup/backups from 2016-09-21/books/"; DSTBK="/media/lucian/Backup/backups from 2016-09-21/books.bak/";
#SRC="/media/BIG/spideroak/"; DST="/media/lucian/Backup/backups from 2016-09-21/spideroak/"; DSTBK="/media/lucian/Backup/backups from 2016-09-21/spideroak.bak/";
#SRC="/media/BIG/pictures/"; DST="/media/lucian/Backup/backups from 2016-09-21/pictures/"; DSTBK="/media/lucian/Backup/backups from 2016-09-21/pictures.bak/";




#SRC="/cygdrive/d/spideroak/myHouse/"; DST="test-data/DST/";
#SRC="/cygdrive/d/exports/2015-08-27 -uTests/"; DST="test-data/DST/";
#SRC="/cygdrive/d/TFD tests/AIR uploader/"; DST="test-data/DST/";

# -- simulate a fist-backup --
#rm -f "$SRC/backup.sqlite"; rm -f "$DST/backup.sqlite";
# -- test whole-copies, for empty backup DST's --
#rm -rf "$DST/"; mkdir -p "$DST";

#echo "calculate local hashes"
python ./test-Hasher-FastContentHashV1Cached.py --verbose=1 --useCache=0 --data="$SRC" --cache="$SRC/backup.sqlite" 

exit;

###echo "compare"
###python ./test-Comparer.py --cacheNew="$SRC/backup.sqlite" --cacheOld="$DST/backup.sqlite" --doApply=0


##echo "compare & update changes"
python ./test-Writer-LocalPathWriter.py --verbose=1 --cacheNew="$SRC/backup.sqlite" --cacheOld="$DST/backup.sqlite" --destination="$DST" --destinationBackup="$DSTBK" --source="$SRC"

exit;
##echo "clean cache"
python ./test-Cache-cleanup.py --cache="$SRC/backup.sqlite" --optimize=1 --removeOldLeafs=1 --verbose=1



##echo "update full hashes"
python ./test-BackupHashUpdater.py --cache="$SRC/backup.sqlite" --data="$SRC" --percent=1 --min=5

##echo "check full hashes"
python ./test-BackupHashChecker.py --cacheOld="$DST/backup.sqlite" --destination="$DST" --source="$SRC" --percent=5 --min=5

##echo "analize cache"
python ./test-BackupAnalyzer.py --cache="$SRC/backup.sqlite" --data="$SRC"


##echo "copy cache"
cp -f "$SRC/backup.sqlite" "$DST/backup.sqlite"
