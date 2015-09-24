import codecs
import re

kana_to_ipa_file = "/export/ws15-pt-data/tkekona/LM/JA/data/kana_to_ipa.txt"
hira_to_kana_file = "/export/ws15-pt-data/tkekona/LM/JA/data/hira_to_kana.txt"
phrase_to_kana_file = "/export/ws15-pt-data/tkekona/LM/JA/data/J_phrase_to_kana.txt"
output_name = "/export/ws15-pt-data/tkekona/LM/JA/data/J_kanji_to_kana.txt"

def main():
	kana_to_ipa = makeDictionary(kana_to_ipa_file, "\t")
	htk = makeDictionary(hira_to_kana_file, "\t")
	phrase_to_kana = makeDictionary(phrase_to_kana_file, "\t")
	set = makeSet(hira_to_kana_file)
	output = open(output_name, 'w')
	
	kanji_dict = {}
	tmp_dict = {}
	
	for key, value in phrase_to_kana.iteritems():
		key2 = key
		value2 = value
		while len(key) != 0 and len(value) != 0 and (key[0] in set) and (key[0] == value[0] or htk[key[0]] == value[0]):
			key = key[1:]
			value = value[1:]
		while len(key) != 0 and len(value) != 0 and (key[-1:] in set) and (key[-1:] == value[-1:] or htk[key[-1:]] == value[-1:]):
			key = key[:-1]
			value = value[:-1]
		kanji = ""
		yomi = ""
		non_kanji = ""
		while len(key) != 0:
			while len(key) != 0 and key[0] not in set:
				kanji += key[0]
				key = key[1:]
				yomi += value[0]
				value = value[1:]
			else:
				while len(key) != 0 and key[0] in set:
					non_kanji += key[0]
					key = key[1:]
				if len(key) != 0:
					lst = value.split(to_kana(non_kanji, htk), 1)
					yomi += lst[0]
					addKY(tmp_dict, kanji, yomi, non_kanji)
					if len(lst) > 1:
						value = lst[1]
					else:
						print (key2 + " " + value2).encode('utf-8')
						key = ""
						value = ""
						tmp_dict = {}
					kanji = ""
					yomi = ""
					non_kanji = ""
				else:
					if len(non_kanji) != 0:
						lst = value.split(to_kana(non_kanji, htk), 1)
						yomi += lst[0]
					else:
						yomi += value
					addKY(tmp_dict, kanji, yomi, non_kanji)
		mergeDicts(kanji_dict, tmp_dict)
###					kanji_dict[kanji] = yomi
		
	for kanji, dict2 in kanji_dict.iteritems():
		output.write((kanji + ":\n").encode('utf-8'))
		for kana, times in dict2.iteritems():
			output.write(("\t" + kana + "\t" + str(times) + "\n").encode('utf-8'))
			
def mergeDicts(kanji_dict, tmp_dict):
	for k, v in tmp_dict.iteritems():
		if k in kanji_dict:
			if v in kanji_dict[k]:
				kanji_dict[k][v] += 1
			else:
				kanji_dict[k] = {v : 1}
		else:
			kanji_dict[k] = {v : 1}
		
def to_kana(non_kanji, htk):
	retn = ""
	for char in non_kanji:
		if char in htk:
			retn += htk[char]
		else :
			retn += char
	return retn
			
	
def addKY(kanji_dict, kanji, yomi, non_kanji):
	if kanji != "":
		if kanji in kanji_dict:
			if yomi in kanji_dict[kanji]:
				kanji_dict[kanji][yomi] += 1
			else:
				kanji_dict[kanji] = {yomi : 1}
		else:
			kanji_dict[kanji] = {yomi: 1}
	
# This is a whitebox method for making a set of all hiragana & katakana using hira_to_kana_file
def makeSet(file):
	set = []
	file = codecs.open(file, 'r', 'utf-8')
	for line in file:
		line = line.strip()
		pair = line.split()
		if len(pair) == 2:
			set.extend(pair)
	return set

def makeDictionary(dictFile, parser):

	#Open the hangarian to API character dictionary
	file = codecs.open(dictFile, 'r', 'utf-8')
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
			print "#" + phone + "#"
			print "#" + phone + "#" + " was not found in PIDict"
	
	return result.strip()
main()