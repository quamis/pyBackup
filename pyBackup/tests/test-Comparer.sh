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

echo "caculate hashes"
python ./test-Hasher-FastContentHashV1Cached.py --verbose=0 --data="test-data/tmp-data/" --cache="test-data/tmp-cache/FileSystem1.sqlite"




echo "initialize v2"

rm -rf "test-data/tmp-data/"
mkdir "test-data/tmp-data/"

echo "re-fill data"
cp -rf "test-data/data-m2/." "test-data/tmp-data/"
find "test-data/tmp-data/" -name ".gitignore" -type f -delete

echo "re-caculate hashes"
python ./test-Hasher-FastContentHashV1Cached.py --verbose=0 --data="test-data/tmp-data/" --cache="test-data/tmp-cache/FileSystem2.sqlite"


echo "compare"
python ./test-Comparer.py --cacheNew="test-data/tmp-cache/FileSystem2.sqlite" --cacheOld="test-data/tmp-cache/FileSystem1.sqlite"

echo "re-compare"
python ./test-Comparer.py --cacheNew="test-data/tmp-cache/FileSystem2.sqlite" --cacheOld="test-data/tmp-cache/FileSystem1.sqlite"

echo "cleanup"
rm -rf "test-data/tmp-cache/"
rm -rf "test-data/tmp-data/"