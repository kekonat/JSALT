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
w2pdict = "/export/ws15-pt-data/tkekona/LM/JA/data/J_best_kanji_to_kana.txt"
k2idict = "/export/ws15-pt-data/tkekona/LM/JA/data/kana_to_ipa.txt"
h2kdict = "/export/ws15-pt-data/tkekona/LM/JA/data/hira_to_kana.txt"
nonkanjiphrases = "/export/ws15-pt-data/tkekona/LM/JA/data/all_non_kanji_lines.txt"
commonpron = "/export/ws15-pt-data/tkekona/LM/JA/data/common_pron.txt"
oovchar = open("/export/ws15-pt-data/tkekona/LM/JA/oovchar_wiki.txt", 'w')
oovpronun = open("/export/ws15-pt-data/tkekona/LM/JA/oovpronun_wiki.txt", 'w')
results = open("/export/ws15-pt-data/tkekona/LM/data/phones/phones_wiki_ja.txt", 'w')
oov = {}	


def main():
	#The current hardcoded locations are for test purposes. These values are overwritten by the
	#input parameters below
	
	ctextlist = "/export/ws15-pt-data/tkekona/LM/data/transcripts/names_list/ja_wiki_transcript_names.txt"

	#Make an words to pronunciation dictionary
	JPDict = makeDictionary(w2pdict, '\t', True)
	#Make a kana to ipa
	KIDict = makeDictionary(k2idict, '\t', True)
	#Chain HPDict and PIDict to make a HWIDict
	JWIDict = chainDictionaries(JPDict, KIDict)
	
	#Make hira to ipa dict
	HKDict = makeDictionary(h2kdict, '\t', True)
	#Chain HPDict and PIDict to make a HWIDict
	HKIDict = chainDictionaries(HKDict, KIDict)
	
	#Make a nonkanji phrases to ipa dictionary
	NKDict = makeDictionary(nonkanjiphrases, '\t', True)
	#Chain HPDict and PIDict to make a HWIDict
	NKIDict = chainDictionaries(NKDict, KIDict)
	
	#Make a common words to ipa dictionary
	CDict = makeDictionary(commonpron, '\t', True)
	#Chain HPDict and PIDict to make a HWIDict
	CIDict = chainDictionaries(CDict, KIDict)
	
	#htextlist contains a list of all the hungarian transcript file names appended with .wav
	with open(ctextlist) as list:
		#Iterate through the htext file names and change text to IPA form
		for line in list:
			toIpa(line.strip(), JWIDict, HKIDict, KIDict, NKIDict, CIDict)
			
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
	
#	Letters are not split by whitespace in japanese
#	#Split the original string by whitespace
#	phonemes = re.split(' ', value.strip())
	
	w = value
	while len(value) != 0:
		while w not in PIDict and len(w) > 1:
			w = w[:-1]
		if w in PIDict:
			result = result + PIDict[w].strip() + " "
		else:
			oovpronun.write("#" + w.encode('utf-8') + "#")
		value = value[len(w):]
		w = value
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
				a = pair[0].strip()
				b = pair[1].strip()
				#This is what was currently used to produce the weird result
				if ('\t' in a) or ('\n' in a) or (a == '') or ('\t' in b) or ('\n' in b) or (b == ''):
					print ("a = #" + a + "#\t b = #" + b + "#").encode('utf-8')
				else:
					dict[a] = b
				#if a != ' ' and a != '\t' and a != '\n' and a != '' and b != ' ' and b != '\t' and b != '\n' and b != '':
				#	dict[a] = b.strip()
				
	return dict
	
def toIpa(jFile, JWIDict, HKIDict, KIDict, NKIDict, CIDict):
	file = codecs.open(jFile.strip(), 'r', 'utf-8')
	for line in file.readlines():
		pron = ""
		words = re.split(r"[\w']+|\s+|\.|\*|\"|\-|\(|\)|\,|[.「」*,、・(\"（）0123456789、，：_ ,“”\"\'$;; :\n#%^^ & -)&=><*@ @-[]]", line)
		for word in words:
			w = word
			while len(word) != 0:
				while len(w) != 0 and w[0] in [u'？','?', u'。', '!']:
					pron = pron + 'sil\n'
					word = word[1:]
					w = word
				if len(w) == 0:
					continue
				while w not in JWIDict and w not in HKIDict and w not in KIDict and w not in NKIDict and w not in CIDict and len(w) > 1:
					w = w[:-1]
				if w in [u'？', u'。', '?', '!']:
					pron = pron + 'sil\n'
				elif w in JWIDict:
					pron = pron + JWIDict[w].strip() + " "
				elif w in NKIDict:
					pron = pron + NKIDict[w].strip() + " "
				elif w in CIDict:
					pron = pron + CIDict[w].strip() + " "
				elif w in HKIDict:
					pron = pron + HKIDict[w].strip() + " "
				elif w in KIDict:
					pron = pron + KIDict[w].strip() + " "
				elif w in oov:
					oov[w] = oov[w] + 1
				else:
					oov[w] = 1
				word = word[len(w):]
				w = word
				
		if len(pron) != 0:
			pron = pron.replace(" ː".decode('utf-8'), "ː".decode('utf-8'))
			pron = pron.replace("ːːːː".decode('utf-8'), "ː".decode('utf-8'))
			pron = pron.replace("ːːː".decode('utf-8'), "ː".decode('utf-8'))
			pron = pron.replace("ːː".decode('utf-8'), "ː".decode('utf-8'))
			pron = pron.replace(" ː".decode('utf-8'), "ː".decode('utf-8'))
			pron = pron.replace("\nː".decode('utf-8'), "\n")
			pron = pron.strip() + "\n"
			#print(pron.encode('utf-8'))
			results.write(pron.encode('utf-8'))
			pron = ""
	
main()