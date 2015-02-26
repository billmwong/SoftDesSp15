"""
Created on Wed Feb 25 2015

Author: Bill Wong

Reads the first 500 the top-level comments from any reddit thread
and prints the top 30 most used words into a cache file along
with their frequency.

Can be pasted directly into worditout.com to generate word clouds.
"""

from pattern.web import *
from stopwords import STOPWORDS     #list of words that we don't care about
import string
import collections

def top_words(url):
	"""
	Gets the text of the top 500 top-level comments of the given reddit thread,
    then returns the top 30 most-frequently used words.

	url: URL of reddit thread to read from
	returns: A string of the top 30 most used words and the number of times each
            is used.
	"""
	newurl = URL(url + '?depth=1&sort=top&limit=500')
                    #only read top-level comments, sort by top, only the first 500 comments
	dom = DOM(newurl.download(cached=True))
	comments = ""
	for e in dom('div.usertext-body')[2:]: # search for the usertext comments
		thiscom = repr(plaintext(e.content))[2:-1]	# strip the content so that just the comment remains
		comments += " " + thiscom # add a space, then add the next comment
	return count_words(comments)   # count the words of all the comments


def count_words(text):
    """
    Analyzes the word frequency of a given block of text.

    text: the text to analyze
    returns: A string of the top 30 most used words and the number of times each
            is used according to the format:
                word1: 100
                word2: 95
                word3: 37
    """
    d = {}
    text = text.replace("\\n"," ")	# remove line breaks
    text = text.lower()	# make everything lowercase
    text = text.replace("\'","")	# delete apostrophes
    text = text.translate(string.maketrans(string.punctuation, ' '*len(string.punctuation)))
                                                #replace punctuation with a space
    word_list = text.split()	# create a list of all the words in the text
    important_words = []
    for word in word_list:
    	if word not in STOPWORDS:
    		important_words.append(word)	# only care about words not in the the STOPWORDS list
    frequency = collections.Counter(important_words).most_common(30)    # count them, and take the 30 most common words
    freq_dict = dict(frequency) # convert to a dictionary
    freq_strs = str(freq_dict)  # convert the dictionary to a string
    res = freq_strs[1:-1]   #strip away the brackets
    res = res.replace("'","")   # remove the quotes
    res = res.replace(", ","\n")    # change commas into new lines
    return res

thisURL = 'http://www.reddit.com/r/IAmA/comments/14cb0c/im_snoop_lion_ask_me_anything/'
words_final = top_words(thisURL)

cache_file = open("cache.txt", "w")
cache_file.write(thisURL)
cache_file.write('\n')
cache_file.write(words_final)
cache_file.close()