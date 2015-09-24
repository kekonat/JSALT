import codecs

destination = "/export/ws15-pt-data/tkekona/LM/data/u_phones"
file_names = "/export/ws15-pt-data/tkekona/LM/PT/phone_file_names.txt"
dictionary = "/export/ws15-pt-data/tkekona/PT/merged_phones.txt"

dict = {}
file = codecs.open(dictionary, 'r', 'utf-8')
for line in file:
	pair = line.split('\t')
	dict[pair[0].strip()] = pair[1].strip()

names_file = open(file_names, 'r')
for name in names_file:
	file = codecs.open(name.strip(), 'r', 'utf-8')
	output_file = name.replace('phones', 'u_phones')
	output = open(output_file.strip(), 'w')
	first = True
	for line in file:
		if not first:
			output.write("\n")
		else:
			first = False
		output_line = ""
		phones = line.split()
		for phone in phones:
			if phone in dict:
				output_line += dict[phone] + " "
			else:
				output_line += phone + " "
		output.write(output_line.encode('utf-8'))
	file.close()
	output.close()