#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import codecs

dict = "/export/ws15-pt-data/haotang/SBS-mul-exp/conf/mandarin/callhome-dict"
name_list = "/export/ws15-pt-data/tkekona/LM/data/transcripts/names_list/zh_wiki_transcript_names.txt"

output = open('oov.txt', 'a')
result = open('no_sil_l5.txt', 'w')

pron_dict = {}
f = codecs.open(dict, 'r', 'utf-8')
for line in f:
	phrase, prons = line.strip().split('\t')
	pron = prons.split(', ')[0]
	pron_dict[phrase] = pron
f.close()

with open(name_list, 'r') as files:
	for file in files.readlines():
		f = codecs.open(file.strip(), 'r', 'utf-8')
		oov = {}
		for line in f:	
			pron = ""
			words = re.split(r"[\w']+|[.「」（）0123456789、，：_ ,“”\"\'$;; :#%^^ & &=><*@ @-[]]", line)
			if len(words) > 5:
				for word in words:
					w = word
					while len(word) != 0:
#						while len(w) != 0 and w[0] in [u'？','?', u'。', '!']:
#								pron = pron + '<sil>\n'
#								word = word[1:]
#								w = word
#						if len(w) == 0:
#							continue
						if len(w) != 0 and w[0] in [u'？','?', u'。', '!']:
								pron = pron + '\n'
								word = word[1:]
								w = word
						if len(w) == 0:
							continue
						while w not in pron_dict and len(w) > 1:
							w = w[:-1]
						if len(w) == 1 and w not in pron_dict:
							if w in [u'？', u'。', '?', '!'] and len(pron) != 0:
								pron = pron + '\n'
							elif w in oov:
								oov[w] = oov[w] + 1
							else:
								oov[w] = 1
							word = word[1:]
							w = word
						else:
							pron = pron + pron_dict[w] + " "
							word = word[len(w):]
							w = word
				if len(pron) != 0:
					pron = pron.strip()
					pron = pron + "\n"
					result.write(pron.encode('utf-8'))
					pron = ""
					#print pron.encode('utf-8')
		f.close()
	for k, p in oov.items():
		output.write((k + "\t" + str(p) + "\n").encode('utf-8'))
