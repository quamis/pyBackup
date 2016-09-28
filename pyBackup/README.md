@2016-02-10
 - split the backup into phases
 - refactor the whole backup procedure
        - pre-ops
            - sql dump (via ssh?)
            - pre-cleanup
                - ???
        - post-ops
            - print some DB stats
                x total files
                x total size
                x avg file size
                x duplicated files
                x 0-length files
                x % of files with fullHash
                x % of files with recovery data
            x cleanups
                x DB VACUUM
                x remove unreferenced data from tags & fullHashes
				
		x re-check that X% of the final backup exists and its hash is valid (check fullHash)
		x compute fullHash for X% of the DB
            - recheck code, arg names, vars, script names
            x generalizat formatPath, facut modular, facut optimizal daca face flush() sau nu
            - when writing, on fileUpdate & delete make backups first
            - write recovery information for X% of the backed files
                - PAR2?
                    https://multipar.eu/
                    https://github.com/Parchive/par2cmdline
                    http://www.irasnyder.com/gitweb/?p=rarslave2.git;a=summary
                    
                    
            - write archives of x% of very old data (unchanged for more than X days?)
 	- path reader
		- these export file lists to be backed up(full path, prefixed by protocol (file://, owncloud://)
		- the file lists are then compared with the file lists on the target device
		- examples:
			x local disk reader
			- webdav/owncloud reader
			- ssh reader
				@see http://docs.pyfilesystem.org/en/latest/
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
				x simple (sha1 from the whole file contents)
				x fast (sha1 from partial file contents, adaptive according to file size)
				x natural (compares filemtime, filesize, fast hash)
            
			

Dependencies:			
	pip install bases.py
	

Dev-tests:
        editor: kdevelop/notepad++

	python ./test-LocalPathReader-LocalPathReader.py
		- test the local path reader

	python ./test-Hasher-FastHashV1.py
		- test the local path reader & fast hasher
		
	python ./test-Hasher-FastHashV1Cached.py
		- test the local path reader & fast hasher & cache
		
	python ./test-Hasher-FastContentHashV1Cached.py --verbose=0 --data="test-data/data-m/" --cache="test-data/tmp-cache/FileSystem1.sqlite"
		- test the local path reader & fast content hasher & cache
		
	
	python ./test-Comparer.py
	./test-Comparer.sh
		- compare 2 databases
		
	python ./test-Writer-LocalPathWriter.py --cacheNew="test-data/tmp-cache/FileSystem2.sqlite" --cacheOld="test-data/tmp-cache/FileSystem1.sqlite" --backup="test-data/tmp-data-backup/" --source="test-data/tmp-data/"
	./test-Writer.sh
		- compare 2 databases, write differences
		
	python ./test-BackupAnalyzer.py --cache="test-data/tmp-cache/FileSystem1.sqlite" --data="/cygdrive/d/exports/2016-01-13 - BSP/"
	./test-BackupAnalyzer.sh
		- analyze the sqlite DB, display some stats
	
	python ./test-BackupHashUpdater.py --cache="test-data/tmp-cache/FileSystem1.sqlite" --data="$SRC" --percent=1 --min=20
	./test-BackupHashUpdater.sh
	./test-BackupHashUpdater-big.sh
		- post-update the full hashes. slow
	
		
		
