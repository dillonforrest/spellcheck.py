#!/usr/bin/python
# inspiration from norvig.com/spell-correct.html

import re, collections

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def makeListOfWords(text):
	listofwords = re.findall('[a-z]+', text.lower())
	return listofwords
def makeWordDict(words):
	#lambda:1 instead of lambda:0 so that new words won't be considered incorrect
	dictofwords = collections.defaultdict(lambda:1)
	for word in words:
		dictofwords[word] += 1
	return dictofwords

textfile = file('text.txt').read()
WORDDICT = makeWordDict(makeListOfWords(textfile))

# find all edits with a "distance" of 1
def editDist1(word):
	split     = [(word[:i], word[i:]) for i in range(len(word)+1)]
	delete    = [a + b[1:] for a, b in split if b]
	transpose = [a + b[1] + b[0] + b[2:] for a, b in split if len(b)>1]
	replace   = [a + c + b[1:]  for a, b in split for c in ALPHABET if b]
	insert    = [a + c + b for a, b in split for c in ALPHABET]
	return set(delete + transpose + replace + insert)

"""
def edits1(word):
	splits = []; deletes = []; transposes = []; replaces = []; inserts = []
	for i in range(len(word)+1):
		splits.append((word[:i],word[i:]))
	for a, b in splits if b:
		deletes.append(a + b[1:])
	for a, b in splits if len(b)>1:
		transposes.append(a + b[1] + b[0] + b[2:])
	for a, b in splits if b:
		for c in ALPHABET:
			replaces.append(a + c + b[1:])
			inserts.append(a + c + b)
	return set(deletes + transposes + replaces + inserts)
"""

# Find real words from edits with a distance of 2, by taking (editDist1)^2
def knownFromEdits(word):
	return set(e2 for e1 in editDist1(word) for e2 in editDist1(e1) if e2 in WORDDICT)

"""
def known_edits2(word):
	edits2 = []
	for e1 in edits1(word):
		for e2 in edits1(e1) if e2 in dictofwords:
			edits2.append(e2)
	return edits2
"""

def knownWordsFromList(words):
	return set(word for word in words if word in WORDDICT)

def correct(word):
	candidates = (knownWordsFromList([word]) or knownWordsFromList(editDist1(word)) or
		knownFromEdits(word) or [word])
	return max(candidates, key=WORDDICT.get)
