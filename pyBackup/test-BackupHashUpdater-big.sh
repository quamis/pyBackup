#!/bin/bash

echo "initialize"

SRC="/media/BIG/books/raw/Romanian.Book.Colection-J4K/"

#echo "caculate hashes"
#rm -rf "test-data/tmp-cache/"; mkdir "test-data/tmp-cache/"
#python ./test-Hasher-FastContentHashV1Cached.py --verbose=0 --data="$SRC" --cache="test-data/tmp-cache/FileSystem1.sqlite"

echo "analize"
python ./test-BackupHashUpdater.py --cache="test-data/tmp-cache/FileSystem1.sqlite" --data="$SRC" --percent=1 --min=1000

echo "analize cache"
python ./test-BackupAnalyzer.py --cache="test-data/tmp-cache/FileSystem1.sqlite" --data="$SRC"
