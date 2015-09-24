# -*- coding: utf-8 -*-
import re
import codecs
import sys, getopt

# This program reads hungarian text and converts it to IPA characters.
# It first reads through the text and tries to find English Words
# If English words are found, uses a pre-made dictionary to map the
# English word to IPA pronunciation syllables
# Any non-English word is then converted to IPA characters using a second
# Dictionary provided by Mark

#Define a file path
w2pdict = "/export/ws15-pt-data/tkekona/cantonese/data/dict.txt"
p2idict = "/export/ws15-pt-data/tkekona/cantonese/data/g2p_dict.txt"
oovchar = open("/export/ws15-pt-data/tkekona/LM/CA/oovchar_sbs.txt", 'w')
oovpronun = open("/export/ws15-pt-data/tkekona/LM/CA/oovpronun_sbs.txt", 'w')
results = open("/export/ws15-pt-data/tkekona/LM/data/phones/phones_sbs_ca.txt", 'w')
oov = {}	


def main():
	#The current hardcoded locations are for test purposes. These values are overwritten by the
	#input parameters below
	
	ctext = "/export/ws15-pt-data/tkekona/LM/data/transcripts/ca_sbs/cantonese.txt"

	#Make an Hungarian words to pronunciation dictionary
	CPDict = makeDictionary(w2pdict, '\t', True)
	#Make a Hungarian pronunciation to Ipa dictionary
	CPIDict = makeDictionary(p2idict, '\t', True)
	#Chain HPDict and PIDict to make a HWIDict
	CWIDict = chainDictionaries(CPDict, CPIDict)
	
	#htextlist contains a list of all the hungarian transcript file names appended with .wav
	toIpa(ctext, CWIDict)
			
	for k, v in oov.iteritems():
		oovchar.write((k + "\t" + str(v) + "\n").encode('utf-8'))
			
def chainDictionaries(LPDict, PIDict):
	#New dictionary mapping from Language words to the IPA pronunciation of the word
	newdict = {}
	
	#For every key, value pair in dict1, convert value to Ipa and map dict1 key to Ipa of value
	for key, value in LPDict.iteritems():
		newValue = pronunciationToIpa(value, PIDict)
		newdict[key] = newValue
		
	return newdict

#value is the string of pronunciation symbols
def pronunciationToIpa(value, PIDict):
	#Result string to return
	result = ""
	
	#Split the original string by whitespace
	phonemes = re.split(' ', value.strip())
	
	#Convert each phone to Ipa. If it doesn't exist, replace with a # and print an error message
	for phone in phonemes:
		if phone in PIDict:
			result += PIDict[phone].strip() + " "
		else:
			oovpronun.write("#" + phone + "#")	
	return result.strip()
	
		
def makeDictionary(dictFile, parser, unicode):
	content = ""
	if unicode:
		#Open the hangarian to API character dictionary
		file = codecs.open(dictFile, 'r', 'utf-8')
		content = file.readlines()
	else:
		#We know these files are in English
		file = open(dictFile)
		content = file.readlines()
	
	#Dictionary to return
	dict = {}
	
	#If hangarian character is found, return API form of character
	for line in content:
		line = line.strip()
		if not line.startswith("#") and not line.startswith(";;;"):
			pair =  re.split(parser, line)
			if len(pair) == 2:
				dict[pair[0].strip()] = pair[1].strip()
				
	return dict
	
def toIpa(cFile, pron_dict):	
	file = codecs.open(cFile.strip(), 'r', 'utf-8')
	pron = ""
	f = file.read()
	words = re.split(r"[\w']+|\s+|\.|\*|\"|\-|\(|\)|\,|[.「」*,(\"（）0123456789、，：_ ,“”\"\'$;; :\n#%^^ & -)&=><*@ @-[]]", f)
	for word in words:
		w = word
		while len(word) != 0:
			while len(w) != 0 and w[0] in [u'？','?', u'。', '!']:
				pron = pron + 'sil\n'
				word = word[1:]
				w = word
			if len(w) == 0:
				continue
			while w not in pron_dict and len(w) > 1:
				w = w[:-1]
			if len(w) == 1 and w not in pron_dict:
				if w in [u'？', u'。', '?', '!']:
					pron = pron + 'sil\n'
				elif w in oov:
					oov[w] = oov[w] + 1
				else:
					oov[w] = 1
				word = word[1:]
				w = word
			else:
				if w in [u'？', u'。', '?', '!']:
					pron = pron + 'sil\n'
				else:
					pron = pron + pron_dict[w] + " "
				word = word[len(w):]
				w = word
	if len(pron) != 0:
		pron = pron.strip() + "\n"
		#print(pron.encode('utf-8'))
		results.write(pron.encode('utf-8'))
	
main()