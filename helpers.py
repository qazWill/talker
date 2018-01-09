# contains functions and objects to improve convenience for small tasks,
# miscellaneous help


# converts list elements to string type
def str_a(old):
	
	array = []
	for item in old:
		array.append(str(item))

	return array	

# splits punctuation from a list of words
# and makes it into a seperate item
def sep_punc(words):

	puncs = ['!', '.', ',', ':', ';', '?']
	new_words = []
	for word in words:

		str = ""
		found = False
		for c in word:

			if not found:
				if c not in puncs:
					str = str + c
				else:
					found = True
					if str != "":
						new_words.append(str)
						str = c
			else:
				str = str + c
			
		new_words.append(str)

	return new_words

# checks for punctuation
def is_punc(word):
	puncs = ['!', '.', ',', ':', ';', '?', '"', "'"]
	return word in puncs


			
			
	
	
	
		
					


 
					
		
