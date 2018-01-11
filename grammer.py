# add conjunctions that and also verbs acting as adjectives and multi word verbs
# also save list of possible parts of speech, and use context to pick right one
# also possesives!

from helpers import *

# will be used to keep track of all possible ways of reading a sentence
class Permutation:

	def __init__(self):

		self.nouns = []
		self.verbs = []
		self.noun_mods = []
		self.verb_mods = []
		self.needy_nouns = []
		self.prep = None
		self.recent = None
		self.needs_subject = True

		self.labels = []

	def copy(self):
		perm = Permutation()
		[perm.nouns, prep1] = self.copy_list(self.nouns)
		[perm.verbs, prep2] = self.copy_list(self.verbs)
		[perm.noun_mods, prep3] = self.copy_list(self.noun_mods)
		[perm.verb_mods, prep4] = self.copy_list(self.verb_mods)
		[perm.needy_nouns, prep5] = self.copy_list(self.needy_nouns)
		perm.recent = self.recent
		perm.needs_subject = self.needs_subject

		if prep1 != None:
			perm.prep = prep1
		if prep2 != None:
			perm.prep = prep2
		if prep3 != None:
			perm.prep = prep3
		if prep4 != None:
			perm.prep = prep4
		if prep5 != None:
			perm.prep = prep5
		
		for label in self.labels:
			perm.labels.append(list(label))	

		return perm

	def copy_list(self, array):
		
		prep = None
		
		new_array = []
		for item in array:
			new_item = [None, []]
			new_item[0] = item[0]
			[new_item[1], new_prep] = self.copy_list(item[1])
			new_array.append(new_item)
			if new_prep != None:
				prep = new_prep
			elif item == self.prep:
				prep = new_array[-1]
		return [new_array, prep]

def get_permutations(label_options):
	
	perms = []
	
	size = 1	
	for labels in label_options:
		size *= len(labels)

	for i in range(0, size):	
		perms.append(Permutation()) 

	for labels in label_options:
		chunk_size = len(perms) / len(labels)
		index = 0
		for label in labels:
			for i in range(0, chunk_size):
				perms[index].labels.append(list(label))	
				index += 1

	return perms
		

def label(sentence, memory):

	# gets words from sentence
	words = sentence.split()

	# initializes the list of labels
	label_perms = []
	groups = []
	for word in words:
		label_perms.append(None)

	# checks memory for any known parts
	complete = True
	for i in range(0, len(words)):
		label_perms[i] = check_mem(words[i], memory)	
		if label_perms[i] == []:
			complete = False

	# if there are gaps try to fill in, then update complete if fixed
	if not complete:
		pass		
	 
	# only use the sentence if there are no gaps for now, later implement guessing strategies
	if complete:

		perms = []
		perms.append(Permutation())

		# iterates through all labels and words
		for i in range(0, len(words)):

			# add permutations for all possibilities
			new_perms = []
			for perm in perms:

				first = True
				print label_perms[i]
				for label in label_perms[i]:
					
					if first:
						first = False
						perm.labels.append(list(label))
					else:
						new_perms.append(perm.copy())
						new_perms[-1].labels.pop()
						new_perms[-1].labels.append(list(label))
			for perm in new_perms:
				perms.append(perm)

			# iterates through all currently viable structure permutations	
			removals = []
			for perm in perms:
			
				if perm.labels[i][0] == "noun":

					# records noun
					perm.nouns.append([i, perm.noun_mods])
					perm.noun_mods = []	
			
					# direct object found, add to most recent verb
					if perm.recent == "verb":
						perm.verbs[-1][1].append(perm.nouns[-1])
		
					# looking for object of preposition	
					elif perm.recent == "prep":
						perm.prep[1].append(perm.nouns[-1])
			
					# multi word noun, a mod for a noun that is a noun means multi word
					elif i > 0 and perm.labels[i - 1][0] == "noun" and words[i] not in ["that", "who", "which"]:
						perm.nouns[-2][1].append(perm.nouns[-1])	
						perm.nouns.pop()

					# if it isnt a multi word noun, and recent was a noun then this is an appositive
					# also need to consider things like, "thats the tool I wanted to buy!"
					# tool is the tool in "I wanted to buy a tool"
					elif perm.recent == "noun":
						perm.nouns[-2][1].append(perm.nouns[-1])
						if words[i] in ["that", "who", "which"]:
							perm.needy_nouns.append(perm.nouns[-1])	
							#print needy_nouns
						perm.nouns.pop()

					if perm.prep != None:
						#print i
						#print perm.prep[1]
						#print perm.verbs[0]
						#print 
						pass

					if perm.needs_subject:
						perm.needs_subject = False
						perm.labels[i][1] = "subject"	
						perm.needy_nouns.append(perm.nouns[-1])
				
					perm.recent = "noun"
					#print "noun:"
						
				elif perm.labels[i][0] == "verb":

					# an article before a verb makes no sense	
					if i > 0 and perm.labels[i - 1][0] == "article":
						removals.append(perm)

					# an adjective before a verb makes no sense	
					if i > 0 and perm.labels[i - 1][0] == "adjective":
						removals.append(perm)
						continue

					perm.verbs.append([i, perm.verb_mods])
					perm.verb_mods = []
					
					# multi word verb like have eaten, a mod for a verb that is a verb marks this
					if i > 0 and perm.labels[i - 1][0] == "verb" and perm.labels[i - 1][1] == "helper":
						perm.verbs[-1][1].append(perm.verbs[-2])	
						perm.verbs.remove(perm.verbs[-2])

					# if a subject needs attaching to the verb its doing
					if len(perm.needy_nouns) > 0:
						perm.needy_nouns[-1][1].append(perm.verbs[-1]) 
						perm.needy_nouns.pop()
					
					perm.recent = "verb"

				elif perm.labels[i][0] == "adjective":
					perm.noun_mods.append([i, []])

				elif perm.labels[i][0] == "adverb":
			 		perm.verb_mods.append([i, []])	

				elif perm.labels[i][0] == "article":

					# an adjective before an article makes no sense	
					if i > 0 and perm.labels[i - 1][0] == "adjective":
						removals.append(perm)
						continue

					perm.noun_mods.append([i, []])

				elif perm.labels[i][0] == "preposition":

					# prep modifies last noun
					if len(perm.verbs) == 0:
						perm.nouns[-1][1].append([i, []]) 					
						perm.prep = perm.nouns[-1][1][-1]

					# prep modifies last verb encountered	
					else:	
						perm.verbs[-1][1].append([i, []])
						perm.prep = perm.verbs[-1][1][-1]

					perm.recent = "prep"

				elif perm.labels[i][0] == "conjunction":
						
					if i > 0 and perm.labels[i][0] == "verb":
						perm.labels[i][1] = "verb"
						perm.verbs[-1][1].append([i, []]) # list of connections made	
					
					perm.recent = "conj"
						
				else:
					pass
			
			# remove all permutations that no longer make grammatical sense	
			for removal in removals:
				perms.remove(removal)
		
		for perm in perms:
			print len(perm.nouns)
			print len(perm.verbs)
			print_main(perm.nouns[0], words, perm.labels)
			print "========="
			print print_main(perm.verbs[0], words, perm.labels)
			print "+++++++++++++++++++++++++"

def check_mem(word, memory):
	perms = []

	if word == "a" or word == "an" or word == "the":
		perms.append(["article"])
	
	if word in ["has", "will", "do", "does", "am", "is", "are", "being", "be", "been", "have", "had"]:
		perms.append(["verb", "helper"])
	
	if memory.find_obj(word) != None:
		perms.append(["noun", ""])
	for verb in memory.verbs:
		if verb.present == word:
			perms.append(["verb", "present"])
		if verb.past == word:
			perms.append(["verb", "past"])
		if verb.past_participle == word:
			perms.append(["adjective", "past participle"])
			perms.append(["verb", "past participle"])
		if verb.get_gerund() == word:
			perms.append(["verb", "gerund"])
	for adj in memory.adjectives:
		if adj.word == word:
			perms.append(["adjective", ""])
	for adv in memory.adverbs:
		if adv.word == word:
			perms.append(["adverb", ""])
	if word in ["to", "from", "above", "below", "in", "on", "beside", "inside", "outside"]:
		perms.append(["preposition", ""])
	if word in ["or", "and", "but", "therefore", "yet", "so"]:
		perms.append(["conjunction", "sentence"])
	if word in ["or", "and"]:
		perms.append(["conjunction", "noun"])

	

	return perms 

def print_main(element, words, labels, level=0):
	print " " * level + words[element[0]] + " - " + labels[element[0]][0]
	if len(element[1]) > 0:
		for new_el in element[1]:
			print_main(new_el, words, labels, level + 1)
