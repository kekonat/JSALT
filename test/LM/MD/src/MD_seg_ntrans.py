#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import codecs

dict = "/export/ws15-pt-data/haotang/SBS-mul-exp/conf/mandarin/callhome-dict"
name_list = "/export/ws15-pt-data/tkekona/LM/data/transcripts/names_list/zh_ntrans_transcript_names.txt"

output = open('oov.txt', 'a')
result = open('/export/ws15-pt-data/tkekona/LM/data/phones/phones_ntrans_zh.txt', 'a')

pron_dict = {}
f = codecs.open(dict, 'r', 'utf-8')
for line in f:
	phrase, prons = line.strip().split('\t')
	pron = prons.split(', ')[0]
	pron_dict[phrase] = pron
f.close()

with codecs.open(name_list, 'r', 'utf-8') as names:
	for name in names:
		f = codecs.open(name.strip(), 'r', 'utf-8')
		oov = {}
		for line in f:	
			pron = ""
			words = re.split(r"[\w']+|[.「」（）0123456789、，：_ ,“”\"\'$;; :#%^^ & &=><*@ @-[]]", line)
			for word in words:
				w = word
				while len(word) != 0:
					while len(w) != 0 and w[0] in [u'？','?', u'。', '!']:
							pron = pron + '<sil>\n'
							word = word[1:]
							w = word
					if len(w) == 0:
						continue
					while w not in pron_dict and len(w) > 1:
						w = w[:-1]
					if len(w) == 1 and w not in pron_dict:
						if w in [u'？', u'。', '?', '!']:
							pron = pron + '<sil>\n'
						elif w in oov:
							oov[w] = oov[w] + 1
						else:
							oov[w] = 1
						word = word[1:]
						w = word
					else:
						if w in [u'？', u'。', '?', '!']:
							pron = pron + '<sil>\n'
						else:
							pron = pron + pron_dict[w] + " "
						word = word[len(w):]
						w = word
			if len(pron) != 0:
				pron = pron + "\n"
			result.write(pron.encode('utf-8'))
				#print pron.encode('utf-8')
		f.close()
#	for k, p in oov.items():
#		output.write((k + "\t" + str(p) + "\n").encode('utf-8'))
