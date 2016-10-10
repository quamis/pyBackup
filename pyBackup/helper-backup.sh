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
    
	if [ "$ACTION" == "backup" ] ; then
		#echo "calculate local hashes"
		python ./Hasher.py --verbose=1 --useCache=0 --data="$SRC" --cache="$SRCDB" || error_exit "cannot hash data"

		###echo "compare"
		###python ./test-Comparer.py --cacheNew="$SRC/backup.sqlite" --cacheOld="$DST/backup.sqlite" --doApply=0


		##echo "compare & update changes" 
		python ./Writer.py --verbose=1 --cacheNew="$SRCDB" --source="$SRC" --cacheOld="$DSTDB" --destination="$DST" --destinationBackup="$DSTBK"  || error_exit "cannot write data"


		##echo "clean cache"
		python ./Cleanup.py --cache="$SRCDB" --optimize=1 --removeOldLeafs=1 --verbose=1 || error_exit "cannot write data"


		##echo "update full hashes"
		python ./HashUpdater.py --verbose=0 --cache="$SRCDB" --data="$SRC" --percent=2.5 --min=15 || error_exit "cannot write data"

		
		##echo "check full hashes"
		python ./HashChecker.py --verbose=0 --cacheOld="$DSTDB" --destination="$DST" --source="$SRC" --percent=2.5 --min=5 || error_exit "cannot write data"

		##echo "copy cache"
		cp -f "$SRCDB" "$DSTDB" || error_exit "cannot write data"
	elif [ "$ACTION" == "compare" ] ; then
		#echo "calculate local hashes"
		echo ""
		echo "Create hashes for ${NAME}"
		python ./Hasher.py --verbose=1 --useCache=0 --data="$SRC" --cache="$SRCDB" || error_exit "cannot hash data"

		###echo "compare"
		python ./Comparer.py --verbose=1 --cacheNew="$SRCDB" --source="$SRC" --cacheOld="$DSTDB" --destination="$DST" --destinationBackup="$DSTBK" || error_exit "cannot compare data"

	elif [ "$ACTION" == "check" ] ; then
		##echo "check full hashes"
		python ./HashChecker.py --verbose=4 --cacheOld="$DSTDB" --destination="$DST" --source="$SRC" --percent=25.0 --min=5 || error_exit "cannot write data"

	elif [ "$ACTION" == "checkAll" ] ; then
		##echo "check full hashes"
		python ./HashChecker.py --verbose=4 --cacheOld="$DSTDB" --destination="$DST" --source="$SRC" --percent=100.0 --min=1 || error_exit "cannot write data"

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
	elif [ "$ACTION" == "analyze" ] ; then
		##echo "analize cache"
		echo ""
		echo ""
		echo "Analysis for ${NAME}"
		echo "        ${SRC}"
		python ./Analyze.py --cache="$SRCDB" --data="$SRC" || error_exit "cannot analyze data"
	else :
		error_exit "invalid action: {$ACTION}"
	fi;
	
}
