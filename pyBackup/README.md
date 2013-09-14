WIP
--------------
- renunta la iterator, si foloseste getAll(), elimina iteratorul intern pt getAll.
	- fa intai delete, si apoi update, apoi insert

TODO
---------------
- incearca sa detectezi fisierele mutate/redenumite (am acelasi hash deja in cache, dar in alt path, sters, si pot fac un move local in backup direct).
- determine an ETA.... somehow:)
- system load protection. Daca load-ul in sistem creste peste X, fa sleep


DONE
--------------
- in fisierul de cache, tine minte si filemtime, filesize pt fisierul original, sa putem determina daca e nevoie o recalculare de hash, sau il putrem folosi pe cel din cache
	- la cache, implementeaza getItem, addItem, updateItem, cu un obiect ca parametru, abstractizesi modul de storage asa
- renunta la a tine lista de fisiere cached in acelasi fisier cu cel de cfg. Foloseste alt fisier, special pt asta. comprima-l pe disc
	