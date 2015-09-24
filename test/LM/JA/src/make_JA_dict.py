import codecs
import re

file_folder = "/export/ws15-pt-data/ldc/japanese/csj/d1/TRN-SJIS"
file_names = "/export/ws15-pt-data/tkekona/LM/JA/data/ja_dictionary_fnames.txt"
#trans = codecs.open('/export/ws15-pt-data/ldc/japanese/csj/d1/TRN-SJIS/A01F0001.trn', 'r', 'shift-jis')

#for line in trans:
#	if line[0] != '%' and (ord(line[0]) < 48 or ord(line[0]) > 57):
#		pair = line.split(' &')
#		output = ""
#		if len(pair) == 2:
#			for thing in pair:
#				output += thing.strip() + "\t"
#			print output.strip().encode('shift-jis')

files = open(file_names, 'r')
for file in files.readlines():
	trans = codecs.open(file.strip(), 'r', 'shift-jis')
	for line in trans:
		if re.search('[a-zA-Z]', line) == None:
			line = line.strip()
			if line[0] != '%' and line[0] != "(" and (ord(line[0]) < 48 or ord(line[0]) > 57):
				pair = line.split(' &')
				output = ""
				if len(pair) == 2:
					output += pair[0].strip() + "\t" + pair[1].strip()
					output = re.sub('[()?]', '', output)
					print output.strip().encode('utf-8')
	