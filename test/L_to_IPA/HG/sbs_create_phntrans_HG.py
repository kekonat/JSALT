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
engPronuncToIpa = "/export/ws15-pt-data/data/misc/eng-ARPA2IPA.txt"
engToPronunciation = "/export/ws15-pt-data/data/misc/eng-cmu-dict.txt"

def main(argv):

	#The current hardcoded locations are for test purposes. These values are overwritten by the
	#input parameters below
	htextlist = "/export/ws15-pt-data/data/lists/hungarian/train.txt"
	hungarianFileFolder = "/export/ws15-pt-data/tkekona/textfiles/hungarian/"
	hungarianToIpa = "Hungarian_ref_orthography_dict.txt"

	try:
		opts, args = getopt.getopt(argv,"hg:u:t:",["g2p=","utts=","transdir="])
	except getopt.GetoptError:
		print 'sbs_create_phntrans_HG.py -g <grammerToPhone> -u <utterances> -t <transcriptDirectory>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'sbs_create_phntrans_HG.py -g <grammerToPhone> -u <utterances> -t <transcriptDirectory>'
			sys.exit()
		elif opt in ("-g", "--g2p"): #hungarian to IPA dictionary
			hungarianToIpa = arg
		elif opt in ("-u", "--utts"): #.txt file list
			htextlist = arg
		elif opt in ("-t", "--transdir"): #actual location 
			hungarianFileFolder = arg

	#Make a English pronunciation in English to English pronunciation in Ipa dictionary
	EPIDict = makeDictionary(engPronuncToIpa, '\t', False)
	EPDict = makeDictionary(engToPronunciation, '  ', False)
	HIDict = makeDictionary(hungarianToIpa, '\t', True)
	#Map Hungarian English Words to Ipa Pronunciation
	HEIDict = chainDictionaries(EPIDict, EPDict)
	
	#htextlist contains a list of all the hungarian transcript file names appended with .wav
	with open(htextlist) as list:
		#Iterate through the htext file names and change text to IPA form
		first = True
		for line in list:
#			I used to have a list of all the .wave files but it is now the list of .txt files
#			line = line[:-4]
#			toIpa(hungarianFileFolder + line + "txt", HEIDict, HIDict, line)
			toIpa(hungarianFileFolder + "/" + line.strip() + ".txt", HEIDict, HIDict, line)
			
def chainDictionaries(EIDict, EPDict):
	#New dictionary mapping from English words to the IPA pronunciation of the word
	newdict = {}
	
	#For every key, value pair in EPDict, convert value to Ipa and map key to Ipa
	for key, value in EPDict.iteritems():
		newValue = englishToIpa(value, EIDict)
		newdict[key] = newValue
		
	return newdict

#value is the string of pronunciation symbols
def englishToIpa(value, EIDict):
	#Result string to return
	result = ""
	
	#Split the original string by whitespace
	phonemes = re.split(' ', value.strip())
	
	#Convert each phone to Ipa. If it doesn't exist, replace with a # and print an error message
	for phone in phonemes:
		if phone in EIDict:
			result += EIDict[phone] + " "
		else:
			result += "# "
			print phone + " was not found in EIDict"
	
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
	
def toIpa(hungarianFile, Edict, dict, line):	
	#Open file with hungarian text and read it as unicode
	hf = codecs.open(hungarianFile, 'r', 'utf-8')
	hwords = hf.read()
	
	#If the line starts or ends with a "-", remove it
	if hwords.startswith("-"):
		hwords = hwords[1:]
	if hwords.endswith("-"):
		hwords = hwords[:-1]
	hwords = hwords.lower()
	
	#Build string to write to output file
	ipa = ""
	
	#Makes a list of the individual words by parsing spaces
	words = re.findall(r"[\w']+|[.,!?;]", hwords)
	
	for word in words:
		if word in Edict:
			ipa += Edict[word].decode('utf-8') + " "
		else:
			#Iterate through each character in hwords and change hangarian characters to API
			for char in word:
				if char == "." or char == "!" or char == "?":
					ipa += "sil "
				#Remove all numbers for now
#				elif 48 <= ord(char) and ord(char) <= 57:
#					ipa += char + " "
#				elif 32 <= ord(char) and ord(char) <= 64 or char == "\n":
					#Remove these characters
					
				elif char in dict:
					ipa += dict[char] + " "
			
	print ipa.encode('utf-8').strip()
	
main(sys.argv[1:])