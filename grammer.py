# add conjunctions that and also verbs acting as adjectives and multi word verbs
# also save list of possible parts of speech, and use context to pick right one
# also possesives!

from helpers import *

def label(sentence, memory):

	# gets words from sentence
	words = sentence.split()

	# initializes the list of labels
	labels = []
	groups = []
	for word in words:
		labels.append("")

	# checks memory for any known parts
	complete = True
	for i in range(0, len(words)):
		labels[i] = check_mem(words[i], memory)	
		if labels[i] == "":
			complete = False

	print complete

	# if there are gaps try to fill in, then update complete if fixed
	if not complete:
		pass		
	 
	# only use the sentence if there are no gaps for now, later implement guessing strategies
	if complete:

		noun = None # noun[0] is the index of the noun, noun[1] is all of its modifiers
		verb = None 

		noun_mods = []
		verb_mods = []

		nouns = []
		verbs = []

		recent = None 
		prep = None # maybe change
		

		for i in range(0, len(words)):
		
			if labels[i][0] == "noun":

				# records noun
				nouns.append([i, noun_mods])
				noun_mods = []
			
				# direct object found, add to most recent verb
				if recent == "verb":
					verbs[-1][1].append(nouns[-1])
			
				if recent == "prep":
					prep[1].append(nouns[-1])
			
				# multi word noun, a mod for a noun that is a noun means multi word
				if i > 0 and labels[i - 1][0] == "noun":
					nouns[-2][1].append(nouns[-1])	
					nouns.pop()
				
				recent = "noun"
						
			elif labels[i][0] == "verb":

				verbs.append([i, verb_mods])
				verb_mods = []

				# multi word verb like have eaten, a mod for a verb that is a verb marks this
				if i > 0 and labels[i - 1][0] == "verb":
					verbs[-2][1].append(verbs[-1])	
					verbs.pop()

				recent = "verb"

			elif labels[i][0] == "adjective":
				noun_mods.append([i, []])
			elif labels[i][0] == "adverb":
			 	verb_mods.append([i, []])	
			elif labels[i][0] == "article":
				noun_mods.append([i, []])
			elif labels[i][0] == "preposition":

				# prep modifies last noun
				if len(verbs) == 0:
					nouns[-1][1].append([i, []]) 					
					prep = nouns[-1][1][-1]

				# prep modifies last verb encountered	
				else:	
					verbs[-1][1].append([i, []])
					prep = verbs[-1][1][-1]

				recent = "prep"
					
			else:
				pass

		print_main(nouns[0], words)
		print "========="
		print print_main(verbs[0], words)

		
				
					
			






	'''# identifies the subject
	subject = find_subject(words, labels)	
	
	# identifies the main verb
	verb = find_main_verb(words, labels)

	# connects the different parts of verbs
	chain = -1
	for i in range(0, len(words)):
		if labels[i][0] == "verb":	
			if chain == -1:
				chain = i
				chain_words = []
			chain_words.append(words[i])
		else:
			if chain != -1:
				groups.append(["verb", "", chain, i - 1])
				chain = -1
	if chain != -1:
		groups.append(["verb", "", chain, len(words)])

	# connects compound nouns	
	chain = -1
	for i in range(0, len(words)):
		if labels[i][0] == "noun":	
			if chain == -1:
				chain = i
				chain_words = []
			chain_words.append(words[i])
		else:
			if chain != -1:
				groups.append(["noun", "", chain, i - 1])
				chain = -1
	if chain != -1:
		groups.append(["noun", "", chain, len(words)])

	# identifies the subject
	subject = find_subject(words, labels)	
	
	# identifies the main verb
	verb = find_main_verb(words, labels)

	# finds modifications to the subject

	# finds modifications to the main verb

	# recursively call function again to find details of the self functioning parts???


	# determines if the sentence is a question or statement
	#is_quest = is_question(words, labels)'''

	print words	
	print labels
	print groups
	
	
	# add infered unknowns to list	

def check_mem(word, memory):

	if word == "a" or word == "an" or word == "the":
		return ["article"]
	
	if word in ["has", "will", "do", "am", "is", "are", "being", "be", "been", "have", "had"]:
		return ["verb", "helper"]
	
	if memory.find_obj(word) != None:
		return ["noun"] 
	for verb in memory.verbs:
		if verb.present == word:
			return ["verb", "present"]
		if verb.past == word:
			return ["verb", "past"]
		if verb.past_participle == word:
			return ["adjective", "past participle"]
		if verb.get_gerund() == word:
			return ["verb", "gerund"]
	for adj in memory.adjectives:
		if adj.word == word:
			return ["adjective", ""] 
	for adv in memory.adverbs:
		if adv.word == word:
			return ["adverb", ""] 
	if word in ["to", "from", "above", "below", "in", "on", "beside", "inside", "outside"]:
		return ["preposition", ""]

	return [""]

def print_main(element, words, level=0):
	print " " * level + words[element[0]]
	if len(element[1]) > 0:
		for new_el in element[1]:
			print_main(new_el, words, level + 1)
