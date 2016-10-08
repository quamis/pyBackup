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


function do_backup {
    NAME="$1";
    SRC="$2";
    
    local DST="${DST_DIR}/${NAME}/";
    local DSTBK="${DST_DIR}/${NAME}.bak/";
    local SRCDB="${SQLITE_DIR}${NAME}.sqlite";
    local DSTDB="${DST_DIR}${NAME}.sqlite";
    
    
    if [ ! -d "$DST" ] ; then
        mkdir -p "$DST";
    fi
    
    if [ ! -d "$DSTBK" ] ; then
        mkdir -p "$DSTBK";
    fi
    
    
    #echo "calculate local hashes"
    python ./Hasher.py --verbose=1 --useCache=0 --data="$SRC" --cache="$SRCDB" || error_exit "cannot hash data"

    ###echo "compare"
    ###python ./test-Comparer.py --cacheNew="$SRC/backup.sqlite" --cacheOld="$DST/backup.sqlite" --doApply=0


    ##echo "compare & update changes" 
    python ./Writer.py --verbose=1 --cacheNew="$SRCDB" --source="$SRC" --cacheOld="$DSTDB" --destination="$DST" --destinationBackup="$DSTBK"  || error_exit "cannot write data"


    ##echo "clean cache"
    python ./Cleanup.py --cache="$SRCDB" --optimize=1 --removeOldLeafs=1 --verbose=1 || error_exit "cannot write data"


    ##echo "update full hashes"
    python ./HashUpdater.py --cache="$SRCDB" --data="$SRC" --percent=2.5 --min=15 || error_exit "cannot write data"

    
    ##echo "check full hashes"
    python ./HashChecker.py --cacheOld="$DSTDB" --destination="$DST" --source="$SRC" --percent=10 --min=15 || error_exit "cannot write data"

    
    ##echo "analize cache"
    #python ./test-BackupAnalyzer.py --cache="$SRC/backup.sqlite" --data="$SRC"


    ##echo "copy cache"
    cp -f "$SRCDB" "$DSTDB" || error_exit "cannot write data"
}

SQLITE_DIR="/media/BIG/tmp/pyBackup.sqlite/";

DST_DIR="/media/lucian/Backup/backups from 2016-09-21/";
#DST_DIR="/media/BIG/tmp/pyBackup/";



do_backup "projects" "/home/lucian/projects/"
do_backup "spideroak" "/media/BIG/spideroak/"
do_backup "pictures" "/media/BIG/pictures/"
do_backup "books" "/media/BIG/books/"
do_backup "music" "/media/BIG/music/"


# -- simulate a fist-backup --
#rm -f "$SRC/backup.sqlite"; rm -f "$DST/backup.sqlite";
# -- test whole-copies, for empty backup DST's --
#rm -rf "$DST/"; mkdir -p "$DST";
