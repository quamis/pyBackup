#!/bin/bash
source "helper-backup.sh"

SQLITE_DIR="/media/BIG/tmp/pyBackup.sqlite/";
DST_DIR="/media/lucian/Backup/backups from 2016-09-21/";
#DST_DIR="/media/BIG/tmp/pyBackup/";


if [ ! -d "$DST_DIR" ]; then
    error_exit "external hdd not mounted"
fi;



do_backup "projects" "/home/lucian/projects/"
