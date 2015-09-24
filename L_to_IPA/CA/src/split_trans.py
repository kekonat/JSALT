import re
import codecs

transcript = "/export/ws15-pt-data/tkekona/cantonese/cantonese_matched_full.txt"
output = "/export/ws15-pt-data/tkekona/cantonese/cantonese_ft_pair.txt"

with codecs.open(transcript, 'r', 'utf-8') as file:
	dict = {}
	for line in file:
		fn = True
		file_name = ""
		transcript = ""
		for char in line:
			if fn:
				if char == ':':
					fn = False
				else:
					file_name += char
			else:
				transcript += char
		dict[file_name] = transcript
	out = open(output, 'w')
	for fn, tr in dict.iteritems():
		out.write((fn + "\t" + tr).encode('utf-8'))
	for fn, tr in dict.iteritems():
		if fn[24] == '0':
			fn = fn[:24] + fn[25:]
		file = open("/export/ws15-pt-data/tkekona/cantonese/cantonese/" + fn + ".txt", 'w')
		file.write(tr.encode('utf-8'))