""" Analyzes the word frequencies in a book downloaded from
	Project Gutenberg

	@author: Bill Wong
	"""

import string, collections

def get_word_list(file_name):
	""" Reads the specified project Gutenberg book.  Header comments,
		punctuation, and whitespace are stripped away.  The function
		returns a list of the words used in the book as a list.
		All words are converted to lower case.
	"""
	f = open(file_name,'r')
	lines = f.readlines()
	curr_line = 0
	while lines[curr_line].find('START OF THIS PROJECT GUTENBERG EBOOK') == -1:
	    curr_line += 1
	lines = lines[curr_line+1:]

	text = ""
	for line in lines:
		text += " "
		text += line

	# text = text.replace("\\n"," ")	# remove line breaks
	text = text.lower()	# make everything lowercase
	text = text.replace("\'","")	# delete apostrophes
	text = text.translate(string.maketrans(string.punctuation, ' '*len(string.punctuation)))
	                                            #replace punctuation with a space
	word_list = text.split()	# create a list of all the words in the text
	# print word_list
	return word_list

def get_top_n_words(word_list, n):
	""" Takes a list of words as input and returns a list of the n most frequently
		occurring words ordered from most to least frequently occurring.

		word_list: a list of words (assumed to all be in lower case with no
					punctuation
		n: the number of words to return
		returns: a list of n most frequently occurring words ordered from most
				 frequently to least frequentlyoccurring
	"""
	frequency = collections.Counter(word_list).most_common(100)    # count them, and take the 30 most common words
	withoutnumbers = []
	for e in frequency:
		withoutnumbers.append(e[0])
	return withoutnumbers

t = get_word_list('pg32325.txt')
print get_top_n_words(t,100)