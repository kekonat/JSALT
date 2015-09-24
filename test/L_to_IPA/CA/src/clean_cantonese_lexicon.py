import re
import codecs

lexicon = "/export/ws15-pt-data/tkekona/cantonese/data/lexicon.txt"

dict = {}

with codecs.open(lexicon, 'r', 'utf-8') as file:
	for line in file:
		things = re.split("\t", line.strip())
		if len(things) >= 3:
			dict[things[0]] = things[2]
		
output = open("/export/ws15-pt-data/tkekona/cantonese/data/dict.txt", 'w')
set = set()
for k, v in dict.iteritems():
	phones = re.split(' ', v.strip())
	new_phone = ""
	for phone in phones:
		if phone[0] != '.' and phone[0] != '_':
			new_phone += phone + " "
			set .add(phone)
	new_phone = new_phone.strip()
	output.write((k + "\t" + new_phone + "\n").encode('utf-8'))

unique_set = open("/export/ws15-pt-data/tkekona/cantonese/data/unique_phones.txt", 'a')
for u in set:
    unique_set.write(u + "\n")