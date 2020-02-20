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

# this is the custom loader for the competition
def load_input(filename):
	num_diff_books = load_file(filename, 0, word=0)
	num_libraries = load_file(filename, 0, word=1)
	num_days = load_file(filename, 0, word=2)

	book_scores = load_file(filename, 1)

	library = []

	for i in range(num_libraries):
		temp_library_dict = {}

		library_line = (2*i) + 2
		num_books = load_file(filename, library_line, word=0)
		num_days_for_signup = load_file(filename, library_line, word=1)
		num_books_shippable = load_file(filename, library_line, word=2)

		book_ids = load_file(filename, library_line + 1)

		temp_library_dict['num of books'] = num_books
		temp_library_dict['num of days'] = num_days_for_signup
		temp_library_dict['num of books shippable'] = num_books_shippable
		temp_library_dict['book id list'] = book_ids

		library.append(temp_library_dict)

	return num_diff_books, num_libraries, num_days, book_scores, library


def load_libraries(filename):
	with open(filename) as f:
		b, l, d = map(int, f.readline().split(' '))
		s = list(map(int, f.readline().split(' ')))
		libraries = list()
		for _ in range(l):
			n, t, m = map(int, f.readline().split(' '))
			books = list(map(int, f.readline().split(' ')))
			libraries.append((n, t, m, books))
		return b, l, d, s, libraries
