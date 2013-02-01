__author__ = 'jherskovic'

import json
import csv
import sys 
import cStringIO
import codecs

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") if isinstance(s, basestring) else s for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

original=open(sys.argv[1], "r").read()
# Reencode in UTF8
original=u'\n'.join( x.decode('utf-8') for x in original.split('\n') )
original=original.replace('masterCards = ', '')
jsonrep=json.loads(original)
del original

print "Converting", len(jsonrep), "cards to a CSV file."
out=open(sys.argv[2], 'w')
fields=['cardType', 'text', 'numAnswers', 'expansion']
outwriter=UnicodeWriter(out, fields) # Ignore the ID field
outwriter.writerow(fields)
for card in jsonrep:
    outwriter.writerow([card[x] for x in fields])

out.close()    
