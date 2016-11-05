#!/bin/bash
source "helper-backup.sh"

SQLITE_DIR="/media/BIG/tmp/pyBackup.sqlite/";
DST_DIR="/media/lucian/Backup/backups from 2016-09-21/";
#DST_DIR="/media/BIG/tmp/pyBackup/";

ACTION="$1";
: ${ACTION:="backup"};


if [ ! -d "$DST_DIR" ]; then
    error_exit "external hdd not mounted"
fi;

sync
########################################################################################################
## local backups #######################################################################################

do_action NAME="projects" SRC="$HOME/projects/" PERIOD="2H"

sync
########################################################################################################
## GEO's backups #######################################################################################

mkdir "$HOME/sshfs/" || error_exit "cannot mkdir"
sshfs user@host:/ "$HOME/sshfs/" -p 22 || error_exit "cannot mount sshfs"

do_action "oc-v01" "$HOME/sshfs/media/mnt/a/1/2/3/4/"

fusermount -u "$HOME/sshfs/" || error_exit "cannot disconnect from ssh"
rmdir "$HOME/sshfs/"


sync
