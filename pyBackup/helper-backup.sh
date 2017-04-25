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


function do_action {
    local NAME SRC PERIOD HASHER
    local "${@}"
    
    local DST="${DST_DIR}/${NAME}/";
    local DSTBK="${DST_DIR}/${NAME}.bak/";
    local SRCDB="${SQLITE_DIR}${NAME}.sqlite";
    local DSTDB="${DST_DIR}${NAME}.sqlite";

    
    : ${PERIOD:="always"};
    : ${HASHER="FastContentHashV2Cached"};

    local SHOULD_RUN=1;
    
    if [ -f "$SRCDB" ]; then
        local V1=`python ./Analyze.py --cache="$SRCDB" --data="$SRC" --mode="flags" | grep "last run" | egrep -o "[0-9].+[0-9]"`;
        V1=`date --date="$V1" +"%s"`;
        local V2=`date +"%s"`;
        local RUN_DIFF=$(( V2 - V1 ));

        local TLM=$(( -1 ));
        SHOULD_RUN=0;
        
        
        PERIOD="always"

        if [ "$PERIOD" == "always" ] ; then
            TLM=$(( -1 ))
        elif [ "$PERIOD" == "1m" ] ; then
            TLM=$(( 60*1 ))
        elif [ "$PERIOD" == "5m" ] ; then
            TLM=$(( 60*5 ))
        elif [ "$PERIOD" == "10m" ] ; then
            TLM=$(( 60*10 ))
        elif [ "$PERIOD" == "15m" ] ; then
            TLM=$(( 60*15 ))
        elif [ "$PERIOD" == "30m" ] ; then
            TLM=$(( 60*30 ))
        elif [ "$PERIOD" == "45m" ] ; then
            TLM=$(( 60*45 ))
        elif [ "$PERIOD" == "1H" ] ; then
            TLM=$(( 60*60*1 ))
        elif [ "$PERIOD" == "2H" ] ; then
            TLM=$(( 60*60*2 ))
        elif [ "$PERIOD" == "4H" ] ; then
            TLM=$(( 60*60*4 ))
        elif [ "$PERIOD" == "6H" ] ; then
            TLM=$(( 60*60*6 ))
        elif [ "$PERIOD" == "8H" ] ; then
            TLM=$(( 60*60*8 ))
        elif [ "$PERIOD" == "12H" ] ; then
            TLM=$(( 60*60*12 ))
        elif [ "$PERIOD" == "1D" ] ; then
            TLM=$(( 60*60*24*1 ))
        elif [ "$PERIOD" == "2D" ] ; then
            TLM=$(( 60*60*24*2 ))
        elif [ "$PERIOD" == "3D" ] ; then
            TLM=$(( 60*60*24*3 ))
        elif [ "$PERIOD" == "4D" ] ; then
            TLM=$(( 60*60*24*4 ))
        elif [ "$PERIOD" == "5D" ] ; then
            TLM=$(( 60*60*24*5 ))
        elif [ "$PERIOD" == "1W" ] ; then
            TLM=$(( 60*60*24*7*1 ))
        elif [ "$PERIOD" == "2W" ] ; then
            TLM=$(( 60*60*24*7*2 ))
        elif [ "$PERIOD" == "1M" ] ; then
            TLM=$(( 60*60*24*7*4 ))
        else
            echo "    ${NAME}: don't know when to back it up"
            exit 1;
        fi;

        if (( RUN_DIFF > TLM )); then
            SHOULD_RUN=1
        fi;
    fi;

    if (( $SHOULD_RUN == 0 )) ; then
        echo "    ${NAME} will not be backed up now. It's too soon."
        return;
    fi;
    
    if [ ! -d "$DST" ] ; then
        mkdir -p "$DST";
    fi
    
    if [ ! -d "$DSTBK" ] ; then
        mkdir -p "$DSTBK";
    fi

    
    if [ "$ACTION" == "backup" ] ; then
        #echo "calculate local hashes"
        python ./Hasher.py --verbose=1 --useCache=0 --data="$SRC" --cache="$SRCDB" --Hasher="$HASHER" || error_exit "cannot hash data"

        ###echo "compare"
        ###python ./test-Comparer.py --cacheNew="$SRC/backup.sqlite" --cacheOld="$DST/backup.sqlite" --doApply=0


        ##echo "compare & update changes" 
        python ./Writer.py --verbose=1 --cacheNew="$SRCDB" --source="$SRC" --cacheOld="$DSTDB" --destination="$DST" --destinationBackup="$DSTBK"  || error_exit "cannot write data, in Writer.py"


        ##echo "clean cache"
        python ./Cleanup.py --cache="$SRCDB" --optimize=1 --removeOldLeafs=1 --verbose=1 || error_exit "cannot write data, in Cleanup.py"


        ##echo "update full hashes"
        python ./HashUpdater.py --verbose=0 --cache="$SRCDB" --data="$SRC" --percent=2.5 --min=15 || error_exit "cannot write data, in HashUpdater.py"


        ##echo "check full hashes"
        #echo "--cacheOld=$DSTDB"; echo "--destination=$DST"echo "--source=$SRC"
        python ./HashChecker.py --verbose=1 --stopOnFirstFail=1 --cacheOld="$DSTDB" --destination="$DST" --source="$SRC" --percent=1.0 --min=5 || error_exit "cannot write data, in HashChecker.py"

        ##echo "copy cache"
        cp -f "$SRCDB" "$DSTDB" || error_exit "cannot write data, in copy db"
        
    elif [ "$ACTION" == "backup-remote" ] ; then
        #echo "calculate local hashes"
        python ./Hasher.py --verbose=1 --useCache=0 --data="$SRC" --cache="$SRCDB" --Hasher="$HASHER" || error_exit "cannot hash data"

        ###echo "compare"
        ###python ./test-Comparer.py --cacheNew="$SRC/backup.sqlite" --cacheOld="$DST/backup.sqlite" --doApply=0


        ##echo "compare & update changes" 
        python ./Writer.py --verbose=5 --cacheNew="$SRCDB" --source="$SRC" --cacheOld="$DSTDB" --destination="$DST" --destinationBackup="$DSTBK" --fail=9 || error_exit "cannot write data, in Writer.py"


        ##echo "clean cache"
        python ./Cleanup.py --cache="$SRCDB" --optimize=1 --removeOldLeafs=1 --verbose=1 || error_exit "cannot write data, in Cleanup.py"


        ##echo "update full hashes"
        python ./HashUpdater.py --verbose=0 --cache="$SRCDB" --data="$SRC" --percent=0.5 --min=1 || error_exit "cannot write data, in HashUpdater.py"


        ##echo "check full hashes"
        #echo "--cacheOld=$DSTDB"; echo "--destination=$DST"echo "--source=$SRC"
        python ./HashChecker.py --verbose=1 --stopOnFirstFail=1 --cacheOld="$DSTDB" --destination="$DST" --source="$SRC" --percent=0.5 --min=1 || error_exit "cannot write data, in HashChecker.py"

        ##echo "copy cache"
        cp -f "$SRCDB" "$DSTDB" || error_exit "cannot write data, in copy db"
        
    elif [ "$ACTION" == "compare" ] ; then
        #echo "calculate local hashes"
        echo ""
        echo "Create hashes for ${NAME}"
        python ./Hasher.py --verbose=1 --useCache=0 --data="$SRC" --cache="$SRCDB" --Hasher="$HASHER" || error_exit "cannot hash data"

        ###echo "compare"
        python ./Comparer.py --verbose=1 --cacheNew="$SRCDB" --source="$SRC" --cacheOld="$DSTDB" --destination="$DST" --destinationBackup="$DSTBK" || error_exit "cannot compare data"

    elif [ "$ACTION" == "cleanup" ] ; then
        ##echo "clean cache"
        python ./Cleanup.py --cache="$SRCDB" --optimize=1 --removeOldLeafs=1 --verbose=1 || error_exit "cannot write data"

        ##echo "copy cache"
        cp -f "$SRCDB" "$DSTDB" || error_exit "cannot write data"

    elif [ "$ACTION" == "hash" ] ; then
        #echo "update full hashes"
        python ./HashUpdater.py --verbose=4 --cache="$SRCDB" --data="$SRC" --percent=25.0 --min=5 || error_exit "cannot write data"

        ##echo "copy cache"
        cp -f "$SRCDB" "$DSTDB" || error_exit "cannot write data"
        
    elif [ "$ACTION" == "hashAll" ] ; then
        #echo "update full hashes"
        python ./HashUpdater.py --verbose=4 --cache="$SRCDB" --data="$SRC" --percent=100.0 --min=1 || error_exit "cannot write data"

        ##echo "copy cache"
        cp -f "$SRCDB" "$DSTDB" || error_exit "cannot write data"
            
    elif [ "$ACTION" == "check" ] ; then
        ##echo "check full hashes"
        python ./HashChecker.py --verbose=4 --stopOnFirstFail=0 --cacheOld="$DSTDB" --destination="$DST" --source="$SRC" --percent=25.0 --min=5 || error_exit "cannot write data"

    elif [ "$ACTION" == "checkAll" ] ; then
        ##echo "check full hashes"
        python ./HashChecker.py --verbose=4 --stopOnFirstFail=0 --cacheOld="$DSTDB" --destination="$DST" --source="$SRC" --percent=100.0 --min=1 || error_exit "cannot write data"

    elif [ "$ACTION" == "checkAllAndRemove" ] ; then
        ##echo "check full hashes"
        OUT="tmp.autoRemove.txt"
        echo "HashChecker ${NAME}"
        python ./HashChecker.py --verbose=1 --stopOnFirstFail=0 --cacheOld="$DSTDB" --destination="$DST" --source="$SRC" --percent=100.0 --min=1 > "$OUT"

        while read LINE; do
                python ./RemoveFile.py --verbose=4 --cache="$SRCDB" --destination="$DST" --source="$SRC" --path="$LINE" --doApply=1
        done <"$OUT"
        rm -f "$OUT"

        ##echo "copy cache"
        cp -f "$SRCDB" "$DSTDB" || error_exit "cannot write data"
            
    elif [ "$ACTION" == "analyze" ] ; then
        ##echo "analize cache"
        echo ""
        echo ""
        echo "----------------------------------------------------------------------------"
        echo "----------------------------------------------------------------------------"
        echo "Analysis for ${NAME}"
        echo "        ${SRC}"
        python ./Analyze.py --cache="$SRCDB" --data="$SRC" || error_exit "cannot analyze data"
        read -s -n 1 -p "Press any key to continue... "
        
    elif [ "$ACTION" == "cleanup-backup" ] ; then
        ##echo "copy cache"

        echo "Remove $DSTDB ?"
        select yn in "Yes" "No"; do
            case $yn in
                Yes ) rm -f "$DSTDB" || error_exit "cannot remove data"; break;;
                No ) break;;
                *) echo "invalid option"; break;;
            esac
        done


        echo "Remove $DST ?"
        select yn in "Yes" "No"; do
            case $yn in
                Yes ) rm -rf "$DST" || error_exit "cannot remove data"; break;;
                No ) break;;
                *) echo "invalid option"; break;;
            esac
        done

        echo "Remove $DSTBK ?"
        select yn in "Yes" "No"; do
            case $yn in
                Yes ) rm -rf "$DSTBK" || error_exit "cannot remove data"; break;;
                No ) break;;
                *) echo "invalid option"; break;;
            esac
        done
        
    elif [ "$ACTION" == "help" ] ; then
        echo "backup system to be sure you don't loose everything when you drop your laptop"
        echo "    backup - (default) backup the configured items"
        echo "    compare - compare the configured items and display an overview, without actually doing the backup"
        echo "    cleanup - vacuum, optimize the DB"
        echo "    hash - create hashes for a part of the DB (25%)"
        echo "    hashAll - create hashes for the whole DB"
        echo "    check - check hashes for a part of the DB (25%)"
        echo "    checkAll - check hashes for the whole DB"
        echo "    checkAllAndRemove - check hashes for the whole DB and automatically remove invalid files from the DB. A new backup should be created after this"
        echo "    analyze - display some stats about the backups"
        echo "    cleanup-backup - completly remove all data regarding the backed-up data(DB, data, data.bak)"

        error_exit "help displayed"
        
    else :
        error_exit "invalid action: '{$ACTION}'. try backup.sh help"
        
    fi;
}
