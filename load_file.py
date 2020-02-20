import os

def load_file(filename, line, word=None, line_separator='\n', word_separator=' ', typecast_to=int):
	with open(filename) as f:
		file_content = f.read()
		line_content = file_content.split(line_separator)[line]
		if word is not None:
			return typecast_to(line_content.split(word_separator)[word])
		else:
			return list(map(typecast_to, line_content.split(word_separator)))

def input_files(folder_name='input', extension='.in'):
	yield list(filter(lambda x: x.endswith(extension), os.listdir(folder_name)))