# add conjunctions that and also verbs acting as adjectives and multi word verbs
# also save list of possible parts of speech, and use context to pick right one
# also possesives!

from helpers import *

# will be used to keep track of all possible ways of reading a sentence
class Permutation:

	def __init__(self):

		# the mods of each word, for example to get modifiers of words[i] look in mods[i]
		self.mods = []

		# the labels for this particular permutation
		self.labels = []
		
		# might not need but oh well
		self.words = []

		# list of things that will need to attach or be attached to something coming later
		# needing - needs something
		# needed - is needed by something 
		self.needed_adjectives = [] # need to modify a noun
		self.needed_verb_adverbs = [] # need to modify a verb
		self.needed_degree_adverbs = [] # need to modify adjectives or other adverbs
		self.needing_nouns = [] # need a verb
		self.needing_preps = [] # need a object of preposition(next noun probably)
		self.needed_preps = [] # preps that aren't modifying anything yet
		
		# the entry point, everything is about this, initially unknown probably first noun though
		self.subject = None
		
	def __str__(self):
		
		return self.str_at(self.subject)

	def str_at(self, i, level=0):
		
		string = " " * level + self.words[i] + " - " + self.labels[i][0]
		for mod in self.mods[i]:
			string += "\n"
			string += self.str_at(mod, level + 1)
		return string

	def copy(self):

		perm = Permutation()

		for mod in self.mods:
			perm.mods.append(list(mod))	
		for label in self.labels:
			perm.labels.append(list(label))	
	
		perm.words = self.words

		perm.needed_adjectives = list(self.needed_adjectives)
		perm.needed_verb_adverbs = list(self.needed_verb_adverbs)
		perm.needed_degree_adverbs = list(self.needed_degree_adverbs)
		perm.needing_nouns = list(self.needing_nouns)
		perm.needing_preps = list(self.needing_preps)
		perm.needed_preps = list(self.needed_preps)
		
		perm.subject = self.subject

		return perm
	
	def get_last_of(self, options):
		i = len(self.labels) - 2 
		while i >= 0:  
			if self.labels[i][0] in options:
				return i
			i -= 1
		return -1

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
		perms[-1].words = words

		# iterates through all labels and words
		for i in range(0, len(words)):

			# add permutations for all new possibilities
			new_perms = []
			for perm in perms:

				first = True
				for label in label_perms[i]:
					
					if first:
						first = False
						perm.labels.append(list(label))
						perm.mods.append([])
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

					# records noun and resets needed_adjectives
					perm.mods[i] += perm.needed_adjectives
					perm.needed_adjectives = []	

					# assume first noun is subject change later if proved wrong
					if perm.subject == None:
						perm.subject = i
						perm.needing_nouns.append(i) # subject needs a verb

					# if there was a recent preposition without a noun, attach this noun to it
					if len(perm.needing_preps) > 0:
						perm.mods[perm.needing_preps.pop()].append(i)
					else:	
						
						# otherwise make sure there isnt a complete prep that needs attaching	
						if len(perm.needed_preps) > 0:
							if perm.labels[perm.needed_preps[-1]][1] == "adjective":
								perm.mods[i].append(perm.needed_preps.pop())

						
				elif perm.labels[i][0] == "verb":

					# records the modifiers of the verb
					perm.mods[i] += perm.needed_verb_adverbs
					perm.needed_verb_adverbs = []

					# if there is a noun in need help it
					if len(perm.needing_nouns) > 0:
						perm.mods[perm.needing_nouns[-1]].append(i)

					# if there is a prep in need help it	
					if len(perm.needed_preps) > 0:
						if perm.labels[perm.needed_preps[-1]][1] == "adverb":
							perm.mods[i].append(perm.needed_preps.pop())


				elif perm.labels[i][0] == "adjective":
				
					# records the mod and attaches adverbs
					perm.needed_adjectives.append(i)
					perm.mods[i] += perm.needed_degree_adverbs
					perm.needed_degree_adverbs = []


				elif perm.labels[i][0] == "adverb":
				
					# if it modifies only verbs	
					if perm.labels[i][1] == "verb":
			 			perm.needed_verb_adverbs.append(i)	
						perm.mods[i] += perm.needed_degree_adverbs
						perm.needed_degree_adverbs = []
		
					# if it is a degree adverb
					if perm.labels[i][1] == "degree":
			 			perm.needed_degree_adverbs.append(i)	


				elif perm.labels[i][0] == "article":

					perm.needed_adjectives.append(i) # maybe change later, but it works for now


				elif perm.labels[i][0] == "preposition":

					perm.needing_preps.append(i)

					# if it acts as an adjective
					if perm.labels[i][1] == "adjective":
						index = perm.get_last_of(["noun", "verb"])
						if perm.labels[index][0] == "verb":
							removals.append(perm)
							continue
						else:
							if index == -1:
								needed_preps.append(i)
							else:
								perm.mods[index].append(i)

					# if it acts as an adverb
					if perm.labels[i][1] == "adverb":
						index = perm.get_last_of(["verb"])
						if index == -1:
							index = perm.get_last_of(["noun"])
							if index == -1:
								perm.needed_preps.append(i)
							else:
								removals.append(perm)
								continue
						else:
							perm.mods[index].append(i)

				elif perm.labels[i][0] == "conjunction":
					pass	

						
				else:
					pass

			
			# remove all permutations that no longer make grammatical sense	
			print removals
			for removal in removals:
				perms.remove(removal)
		
		for perm in perms:
			print perm

def check_mem(word, memory):

	degree_adverbs = ["very", "quite", "so", "too", "extremely"]
	preps = ["to", "from", "above", "below", "in", "on", "beside", "inside", "outside"]

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
			perms.append(["adverb", "verb"])
			if word in degree_adverbs:
				perms[-1][1] = "degree"
	if word in preps:
		perms.append(["preposition", "adjective"])
		perms.append(["preposition", "adverb"])
	if word in ["or", "and", "but", "therefore", "yet", "so"]:
		perms.append(["conjunction", "sentence"])
	if word in ["or", "and"]:
		perms.append(["conjunction", "noun"])

	

	return perms 

