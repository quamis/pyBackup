#!/bin/bash

echo "initialize"

rm -rf "test-data/tmp-cache/"
mkdir "test-data/tmp-cache/"


echo "initialize v1"
rm -rf "test-data/tmp-data/"
mkdir "test-data/tmp-data/"

echo "fill data"
cp -rf "test-data/data-m/." "test-data/tmp-data/"
find "test-data/tmp-data/" -name ".gitignore" -type f -delete

#echo "caculate hashes"
#python ./test-Hasher-FastContentHashV1Cached.py --verbose=0 --data="test-data/tmp-data/" --cache="test-data/tmp-cache/FileSystem1.sqlite"

#echo "analize"
#python ./test-BackupAnalyzer.py --cache="test-data/tmp-cache/FileSystem1.sqlite" --data="test-data/tmp-data/"


echo "caculate hashes"
python ./test-Hasher-FastContentHashV1Cached.py --verbose=0 --data="/cygdrive/d/exports/2016-01-13 - BSP/TINA2 - trunk/_3parties/" --cache="test-data/tmp-cache/FileSystem1.sqlite"

echo "analize"
python ./test-BackupAnalyzer.py --cache="test-data/tmp-cache/FileSystem1.sqlite" --data="/cygdrive/d/exports/2016-01-13 - BSP/"

#echo "cleanup"
#rm -rf "test-data/tmp-cache/"
#rm -rf "test-data/tmp-data/"
