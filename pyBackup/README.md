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
            
			
			
pip install bases.py