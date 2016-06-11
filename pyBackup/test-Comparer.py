# -*- coding: utf-8 -*-
'''
@author: lucian
'''
import pprint
import sqlite3

pp = pprint.PrettyPrinter(indent=4)

dbn = sqlite3.connect('FileSystem.sqlite')
#dbo = sqlite3.connect('FileSystem-old.sqlite')

c = dbn.cursor()
c.execute('ATTACH DATABASE ? AS old', ('FileSystem-old.sqlite', ))

#c.execute('SELECT fn.path, fo.path FROM main.files AS fn INNER JOIN old.files AS fo ON fn.path = fo.path')
#pprint.pprint(c.fetchall())

print "new files:"
c.execute('SELECT path FROM main.files WHERE path NOT IN (SELECT path FROM old.files)')
pprint.pprint(c.fetchall())

print "deleted files:"
c.execute('SELECT path FROM old.files WHERE path NOT IN (SELECT path FROM main.files)')
pprint.pprint(c.fetchall())

print "altered files:"
c.execute('SELECT fn.path, fo.path FROM main.files AS fn INNER JOIN old.files AS fo ON fn.path = fo.path WHERE fo.hash!=fn.hash')
pprint.pprint(c.fetchall())

