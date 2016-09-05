@2016-02-10
 - split the backup into phases
 - refactor the whole backup procedure
        - pre-readers
            - sql dump (via ssh?)
            - pre-cleanup
        - post-readers
            - cleanups
		- re-check that X% of the final backup exists and its hash is valid (including fullHash)
		- compute fullHash for X% of the DB
            - print some DB stats
                - total files
                - total size
                - avg file size
                - duplicated files
                - 0-length files
                - % of files with fullHash
                - % of files with recovery data
 	- path reader
		- these export file lists to be backed up(full path, prefixed by protocol (file://, owncloud://)
		- the file lists are then compared with the file lists on the target device
		- examples:
			- local disk reader
			- webdav/owncloud reader
			- ssh reader
	- backup procedure
		- parses the whole file list to be backed up, reads one by one, adds them to the final archive/target device
		- examples:
			- simulation
			- local disk writer
			- archive writer
			- ssh writer
	- removes old backups, when needed, to clear up some space
	- we need some hashers
		- examples:
			- file hasher
				- simple (sha1 from the whole file contents)
				- fast (sha1 from partial file contents, adaptive according to file size)
				- natural (compares filemtime, filesize, fast hash)
        - dupa backup sa existe post operations
            - re-check X% from the backed up files, do a complete content hash check
            - write recovery information for X% of the backed files
            - write archives of x% of very old data (unchanged for more than X days?)
            
			

Dependencies:			
	pip install bases.py
	

Dev-tests:
        editor: kdevelop/notepad++

	test-LocalPathReader-LocalPathReader.py
		- test the local path reader

	test-Hasher-FastHashV1.py
		- test the local path reader & fast hasher
		
	test-Hasher-FastHashV1Cached.py
		- test the local path reader & fast hasher & cache
		
	test-Hasher-FastContentHashV1Cached.py
		- test the local path reader & fast content hasher & cache
		
	
	test-Comparer.py
		- compare 2 databases
	
	
	
--------------------------------------------------
lucian@lucian-P35-DS3:~/projects/pyBackup/pyBackup$ ./test-Comparer.sh 
initialize
initialize v1
fill data
caculate hashes
LocalPathReaderCached.initialize False
sqlite.initialize
LocalPathReaderCached.initialize False
initialize v2
re-fill data
re-caculate hashes
LocalPathReaderCached.initialize False
sqlite.initialize
LocalPathReaderCached.initialize False
compare
moved files:
    ren test-data/tmp-data/2/22/03044_velocityii_1920x1080.jpg --> test-data/tmp-data/1/copyfrom-22/03044_velocityii_1920x1080.jpg
    ...marked
    ren test-data/tmp-data/2/23/werewolf-amazing-hd-wallpapers.jpg --> test-data/tmp-data/1/copyfrom-23/werewolf-amazing-hd-wallpapers.jpg
    ...marked
    ren test-data/tmp-data/file003.txt --> test-data/tmp-data/file003m.txt
    ...marked
    ren test-data/tmp-data/file020.txt --> test-data/tmp-data/file021.txt
    ...marked
deleted files:
changed files:
    upd test-data/tmp-data/file010.txt --> test-data/tmp-data/file010.txt
    ...updated
    upd test-data/tmp-data/03046_theperfectmoment_1920x1080.jpg --> test-data/tmp-data/03046_theperfectmoment_1920x1080.jpg
    ...updated
new files:
cleanup
lucian@lucian-P35-DS3:~/projects/pyBackup/pyBackup$ ./test-Comparer.sh 
