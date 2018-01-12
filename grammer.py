# add conjunctions that and also verbs acting as adjectives and multi word verbs
# also save list of possible parts of speech, and use context to pick right one
# also possesives!

from helpers import *

pronouns = ["I", "you", "he", "she", "it", "we", "they", "us", "them", "those", "these", "this", "that"]

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
		self.subject_skips = 0
		
	def __str__(self):
		
		return self.str_at(self.subject)

	def str_at(self, i, level=0):
		if i == None:
			return "blank sentence"	
		string = " " * level + self.words[i] + " - " + self.labels[i][0]
		string += "(" + self.labels[i][1] + ")"
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
		perm.subject_skips = self.subject_skips

		return perm
	
	def get_last_of(self, options):
		i = len(self.labels) - 2 
		while i >= 0:  
			if self.labels[i][0] == "noun":
				if self.labels[i][1] == "possesive":
					i -= 1
					continue
				if self.labels[i][1] == "compound":
					if self.has_possesive(i):
						i -= 1
						continue
			if self.labels[i][0] in options:
				return i
			i -= 1
		return -1

	def has_possesive(self, i):
		while i < len(self.labels) and self.labels[i][1] == "compound":
			i += 1
		if i < len(self.labels):
			if self.labels[i] == "possesive":
				return True
		return False

	# checks to see if the sentence is valid, need slang incompletes too though
	def valid(self):

		# makes sure there is a subject that has a verb
		if self.subject == None:
			return False
		found = False
		for mod in self.mods[self.subject]:
			if self.labels[mod][0] == "verb":
				found = True	
		if not found:
			return False

		# makes sure all words get used		
		hanging = self.get_hanging(self.subject)
		if len(hanging) > 0:
			return False 

		return True 

	def get_hanging(self, i, words=None):
		if words == None:
			words = range(0, len(self.words))	
		if i in words:
			words.remove(i) 
		for mod in self.mods[i]:
			words = self.get_hanging(mod, words)
		return words

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
				
				#print perm
				#raw_input("...")
			
				if perm.labels[i][0] == "noun":

					# records noun and resets needed_adjectives
					perm.mods[i] += perm.needed_adjectives
					perm.needed_adjectives = []	
					
					# treat as adjective if its a possesive noun
					if perm.labels[i][1] == "possesive":
						perm.needed_adjectives.append(i)
						perm.subject_skips += 1

					# pronouns don't have adjectives
					if perm.words[i] in pronouns and len(perm.mods[i]) > 0:
						removals.append(perm)
						continue

					# assume first noun is subject change later if proved wrong
					if perm.subject == None:
						if perm.subject_skips > 0:
							perm.subject_skips -= 1
						else:	
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

					# if this isn't a single noun and its the end, that can't work
					if i >= len(perm.words) - 1 and perm.labels[i][1] not in ["single"]:
						removals.append(perm)
						continue

					# if there are trailing adverbs then attach to last verb
					if len(perm.needed_verb_adverbs) > 0:
						index = perm.get_last_of("verb") 
						if index != -1:
							perm.mods[index] += perm.needed_verb_adverbs
							perm.needed_verb_adverbs = []


					# checks what the last key element was
					index = perm.get_last_of(["prep", "noun", "verb"])
					if index != -1:

						# must be an appositive, compound noun, or something like "the shirt my friend likes"
						if perm.labels[index][0] == "noun":
							perm.mods[index].append(i)							
							
							# if the last noun is labeled as single that obviously is wrong
							if perm.labels[index][1] in ["single"]:
								removals.append(perm)
								continue

							if perm.labels[index][1] == "compound":

								perm.mods[index].pop()
								perm.mods[i].append(index)

								# if there is an adjective then cant be a compound	
								if len(perm.mods[i]) > 0:
									removals.append(perm)
									continue
	
								# these can't be in a compound
								if perm.words[i] in ["that", "which", "who"]:
									removals.append(perm)
									continue

							if perm.labels[index][1] == "appositive":

								# these can't be in an appositive 
								if perm.words[i] in ["that", "which", "who"]:
									removals.append(perm)
									continue
				

							# if last noun was expecting a direct object clause then this noun needs a verb
							if perm.labels[index][1] == "do_clause" or perm.labels[index][1] == "rel_clause_do":
								perm.needing_nouns.append(i)
								
								# don't want a that occuring after a clauses subj
								if perm.words[i] in ["that", "which", "who"]:
									removals.append(perm)
									continue
						
							# if last noun was expecting a relative object clause then this noun should be who which or that 
							if perm.labels[index][1] == "rel_clause":
							
								# remove perms that don't have the right pronouns or that have adjectives
								if perm.words[i] not in ["who", "which", "that"]:
									removals.append(perm)
									continue								
								if perm.labels[i][1] not in ["rel_clause_do", "rel_clause_sub"]:
									removals.append(perm)
									continue	
								if len(perm.mods[i]) > 0:
									removals.append(perm)
									continue
								
								# if this is the relative clause subject, then it needs a verb
								if perm.labels[i][1] == "rel_clause_sub":
									perm.needing_nouns.append(i)


							# remove rel_clause do's and sub's from non_rel clauses
							else:
								if perm.labels[i][1] in ["rel_clause_do", "rel_clause_sub"]:
									removals.append(perm)
									continue

							# it already has a subject this shouldn't be here
							if perm.labels[index][1] == "rel_clause_sub":
								removals.append(perm)
								continue
								

						if perm.labels[index][0] == "verb":
						
							# if its a direct object
							if perm.labels[i][1] not in ["compound", "possesive"]:
								perm.mods[index].append(i)

							# might need...
							if perm.labels[i][1] == "rel_clause_do":	
								pass


						
				elif perm.labels[i][0] == "verb":

					# records the modifiers of the verb
					perm.mods[i] += perm.needed_verb_adverbs
					perm.needed_verb_adverbs = []

					# if there is a noun in need, help it
					if len(perm.needing_nouns) > 0:
						perm.mods[perm.needing_nouns.pop()].append(i)

					# if there is a prep in need, help it	
					if len(perm.needed_preps) > 0:
						if perm.labels[perm.needed_preps[-1]][1] == "adverb":
							perm.mods[i].append(perm.needed_preps.pop())

					index = perm.get_last_of(["prep", "noun", "verb"])
					if index != -1:

						if perm.labels[index][0] == "noun":

							# if last key word was compound noun or appositive its wrong
							if perm.labels[index][1] in ["compound", "appositive", "rel_clause", "do_clause", "rel_clause_do"]:
								removals.append(perm)
								continue

						if perm.labels[index][0] == "verb":
							pass

					


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
					elif perm.labels[i][1] == "degree":
			 			perm.needed_degree_adverbs.append(i)	


				elif perm.labels[i][0] == "article":

					perm.needed_adjectives.append(i) # maybe change later, but it works for now


				elif perm.labels[i][0] == "prep":

					perm.needing_preps.append(i)

					# if it acts as an adjective
					if perm.labels[i][1] == "adjective":
						index = perm.get_last_of(["noun", "verb"])
						if index == -1:
							removals.append(perm)
							continue
						else:
							if perm.labels[index][0] == "verb":
								removals.append(perm)
								continue
							else:
								perm.mods[index].append(i)

					# if it acts as an adverb
					if perm.labels[i][1] == "adverb":
						index = perm.get_last_of(["verb"])
						if index == -1:
							index = perm.get_last_of(["noun"])
							if index == -1:
								perm.needed_preps.append(i)
								perm.subject_skips += 1
							else:
								removals.append(perm)
								continue
						else:
							perm.mods[index].append(i)

					index = perm.get_last_of(["prep", "noun", "verb"])
					if index != -1:

						if perm.labels[index][0] == "noun":

							# if last key word was compound noun or appositive its wrong
							if perm.labels[index][1] in ["compound", "appositive", "relative", "do_clause", "rel_clause"]:
								removals.append(perm)
								continue

						if perm.labels[index][0] == "verb":
							pass

				elif perm.labels[i][0] == "conjunction":
					pass	

						
				else:
					pass
			
			# remove all permutations that no longer make grammatical sense	
			for removal in removals:
				perms.remove(removal)

		# final grammer pruning
		removals = []
		for perm in perms:
			
			# if there are trailing adverbs then attach to last verb
			if len(perm.needed_verb_adverbs) > 0:
				index = perm.get_last_of("verb") 
				if index != -1:
					perm.mods[index] += perm.needed_verb_adverbs
					perm.needed_verb_adverbs = []

			if not perm.valid():
				removals.append(perm)			
		for removal in removals:
			perms.remove(removal)
		
		for perm in perms:
			print perm

def check_mem(word, memory):

	degree_adverbs = ["very", "quite", "so", "too", "extremely"]
	preps = ["to", "from", "above", "below", "in", "on", "beside", "inside", "outside", "up", "down"]

	perms = []

	if word == "a" or word == "an" or word == "the":
		perms.append(["article", ""])
	
	if word in ["was", "were", "has", "have", "had", "will", "do", "does", "am", "is", "are", "being", "be", "been"]:
		perms.append(["verb", "helper"])

	if word in ["was", "were", "is", "are", "being", "be", "been"]:
		perms.append(["verb", "copula"])
	
	if memory.find_obj(word) != None:
		perms.append(["noun", "single"])
		if word not in ["which", "who", "that"]:
			perms.append(["noun", "compound"]) # like post office
			perms.append(["noun", "appositive"]) # like the man the myth the legend
			perms.append(["noun", "do_clause"]) # direct object clause, example "The food I like" 
			perms.append(["noun", "rel_clause"]) # relative clause The food that ...
	if word in ["my", "his", "her", "our", "their", "your"]:
		perms.append(["adjective", "possesive"])
	if len(word) > 1 and (word[-1] == "'" or word[-2] == "'"):
		perms.append(["noun", "possesive"])
	if word	in ["that", "who", "which"]:
		perms.append(["noun", "rel_clause_do"]) # direct obj of relative clause
		perms.append(["noun", "rel_clause_sub"]) # sub of relative clause
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
		if adj.get_adverb() == word:
			perms.append(["adverb", "verb"])
	for adv in memory.adverbs:
		if adv.word == word:
			perms.append(["adverb", "verb"])
			if word in degree_adverbs:
				perms[-1][1] = "degree"
	if word in degree_adverbs:
		perms.append(["adverb", "degree"])
	if word in preps:
		perms.append(["prep", "adjective"])
		perms.append(["prep", "adverb"])
	if word in ["or", "and", "but", "therefore", "yet", "so"]:
		perms.append(["conjunction", "sentence"])
	if word in ["or", "and"]:
		perms.append(["conjunction", "noun"])

	

	return perms 

