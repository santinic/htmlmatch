#!/usr/bin/env python

import sys
import urllib2
from BeautifulSoup import BeautifulSoup, Tag, NavigableString
import HTMLParser

def htmlmatch(page, pattern):
	"""Finds all the occurrencies of the pattern tree into the given html page"""
	isoup = BeautifulSoup(page)
	psoup = BeautifulSoup(pattern)

	def untiltag(gen):
		node = gen.next()
		while True:
			if isinstance(node, Tag):
				break
			elif len(node.lstrip()) == 0:
				node = gen.next()
			else:
				break
		return node

	pgen = psoup.recursiveChildGenerator()
	pnode = untiltag(pgen)
	igen = isoup.recursiveChildGenerator()
	inode = untiltag(igen)

	variables = []
	lastvars = {}

	while True:
		newvars = nodematch(inode, pnode)
		if newvars != None:
			if len(newvars) > 0:
				lastvars.update(newvars)
			try:
				pnode = untiltag(pgen)
			except StopIteration:
				pgen = psoup.recursiveChildGenerator()
				pnode = untiltag(pgen)
				if len(lastvars) > 0:
					variables.append(lastvars)
					lastvars = {}
		else:
			pgen = psoup.recursiveChildGenerator()
			pnode = untiltag(pgen)
		try:
			inode = untiltag(igen)
		except StopIteration:
			if variables != None:
				return variables
			return None
	return variables

def nodematch(input, pattern):
	"""Matches two tags: returns True if the tags are of the same kind, and if
	the first tag has AT LEAST all the attributes of the second one
	(the pattern) and if these attributes match as strings, as defined in
	strmatch function."""
	if input.__class__ != pattern.__class__:
		return None
	if isinstance(input, NavigableString):
		return strmatch(input, pattern)
	if isinstance(input, Tag) and input.name != pattern.name:
		return None
	variables = {}
	for attr, value in pattern._getAttrMap().iteritems():
		if input.has_key(attr):
			newvars = strmatch(input.get(attr), value)
			if newvars != None:
				variables.update(newvars)
			else:
				return None
		else:
			return None
	return variables

def strmatch(input, pattern):
	"""Matches the input string with the pattern string. For example:

	input: 	 "python and ocaml are great languages"
	pattern: "$lang1$ and $lang2$ are great languages"

	gives as output the map:
	{"lang1": "python", "lang2": "ocaml"}

	The function returns None if the strings don't match."""
	var, value = None, None
	i, j = 0, 0
	map = {}
	input_len = len(input)
	pattern_len = len(pattern)
	while i < input_len:
		if var == None:
			if pattern[j] == '$':
				var = ""
				value = ""
				j += 1
			elif input[i] != pattern[j]:
				return None
			else:
				i += 1
				j += 1
		else:
			while pattern[j] != '$':
				var += pattern[j]
				j += 1;
			j += 1
			if j == pattern_len:
				while i < input_len:
					value += input[i]
					i += 1
			else:
				while i < input_len and input[i] != pattern[j]:
					value += input[i]
					i += 1
			i +=1
			j +=1
			map[var] = value
			var = None
	return map

def main(argv):
	if len(argv) < 2:
		print "example: ./htmlmatch.py input.html pattern.html"
		return
	page = open(argv[0], "r")
	pattern = open(argv[1], "r")
	l = htmlmatch(page, pattern)
	for m in l:
		for k, v in m.iteritems():
			print k, v
		print

if __name__ == "__main__":
    main(sys.argv[1:])
