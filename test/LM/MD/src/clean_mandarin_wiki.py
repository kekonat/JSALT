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

def main():

	#The current hardcoded locations are for test purposes. These values are overwritten by the
	#input parameters below
	htextlist = "/export/ws15-pt-data/tkekona/LM/data/transcripts/names_list/zh_wiki_transcript_names.txt" 	#list of file names
	writeCleanTo = "/export/ws15-pt-data/tkekona/LM/data/transcripts/zh_wiki_clean/zh_wiki_clean.txt"
	#hungarianFileFolder = "/export/ws15-pt-data/tkekona/LM/data/transcripts/hung_wiki/"	#directory holding file
	
	output = open(writeCleanTo, 'a')
	
	with open(htextlist) as list:
		first = True
		for line in list:
			clean(line.strip(), output)
			
def clean(file, output):	

	with codecs.open(file, 'r', 'utf-8') as f:
		tag = False
		close = 0
		for line in f:
			out = ""
			for char in line:
				if tag:
					if char == ">":
						close = close + 1
						if close == 2:
							tag = False
							close = 0
						
				elif char == "<":
					tag = True
				elif ord(char) >= 65 and ord(char) <= 90:
					continue
				elif ord(char) >= 97 and ord(char) <= 122:
					continue
				else:
					out = out + char
			out = out.strip() + "\n"
			output.write(out.encode('utf-8'))

main()