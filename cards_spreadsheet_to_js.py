__author__ = 'jherskovic'

import json
import csv
import sys 
import cStringIO
import codecs

cards=[]

original=open(sys.argv[1], "r")
orig_reader=csv.DictReader(original)
already_seen=set()

punctuation=set([',', '.', '!', '?', '\'', '"'])

def pseudo_hash_card_text(text):
    global punctuation
    text=text.strip()
    for p in punctuation:
        text=text.replace(p, '')
    text=text.replace(' ', '')
    text=text.lower()
    return text

# Eliminate duplicates while reading
for row in orig_reader:
    print row
    this_text=pseudo_hash_card_text(row['text'])
    if this_text not in already_seen:
        cards.append(row)
        already_seen.add(this_text)

original.close()

#Capitalize and punctuate properly; add ids
id_counter=1
for c in xrange(len(cards)):
    this_card=cards[c]
    this_card['id']=str(id_counter)
    id_counter+=1
    if this_card['expansion'] == 'ArsAH':
        this_card['text']=this_card['text'][0].upper() + this_card['text'][1:]
        if this_card['text'][-1] not in punctuation:
            this_card['text'] += '.'
    cards[c]=this_card

print "Converting", len(cards), "cards to a js file."
out=open(sys.argv[2], 'w')
out.write('masterCards = ')
out.write(json.dumps(cards, separators=(', ', ': '), indent=4))
out.close()    
