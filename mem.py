from helpers import *

# This class will contain links to information about itself as well as
# how it relates to other objects in the form of a dependency tree.
class Object: 

	def __init__(self, word):
	
		# the two forms of the word describing this object	
		self.word = word 
	
		# objects directly related to this one
		self.parents = []
		self.children = []

		# what this object does
		self.actions = []

		# type of thought part
		self.type = "object"

	def add_action(self, act):
	
		self.add_action2(self.actions, act)
	
		# important!!!  need to search parents too!!!	


	def add_action2(self, actions, cur):
		found = False
		for act in actions:
			if act.word == cur:
				found = True
				add_action2(act.children, cur[1:])
				break
		if not found: # add here
			add_action_to(actions, cur)
		return found

	def add_action_to(actions, act):
		head = None
		last = None
		first = True
		for item in act:
			cur = Action(item)
			cur.parent = last
			if first:
				actions.append(cur)
				first = False
			else:
				last.children.append(cur)
			last = cur
		last.append(Action("|||"))
				
class Verb:

	def __init__(self, words):

		# default form is plural, write a conversion function
	
		self.word = words[0]
		self.present = words[1] 
		self.past = words[2] 
		self.past_participle = words[3] 

	def forms(self):
		
		forms = []
		forms.append(get_infinitive())
		forms.append(get_gerund())
		forms.append(get_past())
		forms.append(get_present())
		forms.append(get_future())

		# add rest when functions are ready and add singular and plural column
		# also add past, present, future filter
		# and passive active filter

	def get_infinitive(self):
		return "to " + self.present
	
	def get_gerund(self):
		if self.present[-1] == "e":
			return self.present[:-1] + "ing"
		if self.present[-1] == "n":
			return self.present + "ning"
		if self.present[-1] == "m":
			return self.present + "ming"
		return self.present + "ing"	

	def get_past(self):
		return self.past

	def get_present(self):
		return self.present

	def get_future(self):
		return "will " + self.present
	
	def get_progressive_past(self):
		return "have been " + self.get_gerund()

	def get_progressive_present(self):
		return "are " + self.get_gerund()

	def get_progressive_future(self):
		return "will be " + self.get_gerund()

			
class Adjective:

	def __init__(self, word):
		
		self.word = word
			
class Adverb:

	def __init__(self, word):
		
		self.word = word
			

class Action:
	
	def __init__(self, word):
	
		self.word = word # text or address of word 
		
		self.children = []

		self.parent = None



# This class will provide methods to load and save all the information
# that the program needs.  It will also be used for deleting
# unnecessary information as well.
class Memory:

	def __init__(self, obj_file):

		self.obj_file_name = obj_file 
		self.objects = []
		self.verbs = []
		self.adjectives = []
		self.adverbs = []
		self.other = []
		self.load()

	def add_noun(self, word):
		if self.find_obj(word) == None:
			self.insert_word(Object(word), self.objects)

	def add_verb(self, words):
		if self.find_word(words[0], self.verbs) == None:
			self.insert_word(Verb(words), self.verbs)

	def add_adjective(self, word):
		if self.find_word(word, self.adjectives) == None:
			self.insert_word(Adjective(word), self.adjectives)

	def add_adverb(self, word):
		if self.find_word(word) == None:
			self.insert_word(word, self.adverb)

	def load(self):
		file = open(self.obj_file_name, 'r')
		org_lines = file.readlines()
		lines = []
		for line in org_lines:
			lines.append(line.split("\n")[0])
		index = 0
		last = None
		for line in lines:
			words = line.split("|")
			if words[-1] == "":
				words.pop()
			if index == 0:
				for word in words:
					self.objects.append(Object(word))
			elif index == 1:
				for word in words:
					forms = word.split("~")
					self.verbs.append(Verb(forms))
			elif index == 2:
				for word in words:
					self.adjectives.append(Adjective(word))
			elif index == 3:
				for word in words:
					self.adverbs.append(Adverb(word))
			else:
				if index % 2 == 0:
					last = self.find_obj(words[0]) 
					for word in words[1:]:
						for obj in self.objects:
							if obj.word == word:
									last.children.append(obj)
									obj.parents.append(last)
									break
				else:
					pass
			index += 1
		file.close()
		
		'''for item in self.objects:
			print item.word
			print "_________"
			for child in item.children:
				print child.word
			print "=========="
			for parent in item.parents:
				print parent.word
			print'''

	def save(self):
		txt = ""
		for obj in self.objects:
			txt = txt + obj.word + "|"
		txt = txt + "\n"
		for verb in self.verbs:
			txt = txt + verb.word + "~" + verb.present + "~" + verb.past + "~" + verb.past_participle + "|"
		txt = txt + "\n"
		for adj in self.adjectives:
			txt = txt + adj.word + "|"
		txt = txt + "\n"
		for adv in self.adverbs:
			txt = txt + adv.word + "|"
		txt = txt + "\n"
		for obj in self.objects:
			txt	= txt + obj.word + "|"
			for child in obj.children:
				txt = txt + child.word + "|"
			txt = txt + "\n"
			txt = txt + self.actions_to_txt(obj.actions)
			txt = txt + "\n"
		file = open(self.obj_file_name, 'w')
		file.write(txt)
		file.close()

	def actions_to_txt(self, actions):
		txt = str(len(actions))
		txt = txt + "|"
		for act in actions:
			txt = txt + act.word + "|"
			txt = txt + self.actions_to_txt(act.children)
		return txt
			

	# add an action that an object does
	def add_action(obj, action):

		obj = self.find_obj(obj)
		act = self.find_act(obj, act)

		if act == None: # need to add it
			obj.add_action(action)
			

	# adds the pair to the tree heirarchy
	def add_obj(self, child_word, parent_word):

		parent = self.find_obj(parent_word)	
		child = self.find_obj(child_word)
		
		if parent == None:
			parent = Object(parent_word)
			self.insert_obj(parent)
			if child == None:
				child = Object(child_word)
				self.insert_obj(child)
			parent.children.append(child)
			child.parents.append(parent)
		
		else:
			if child == None:
				child = Object(child_word)
				self.insert_obj(child)
				parent.children.append(child)
				child.parents.append(parent)
			else:
				
				if not self.is_descendant(child, parent):
					parent.children.append(child)
					child.parents.append(parent)	
					for descendant in self.get_descendants(parent):
						self.remove_duplicates(descendant, descendant)	

	def get_descendants(self, ancester):
		descendants = []
		for child in ancester.children:
			descendants.append(child)
			for descendant in self.get_descendants(child):
				descendants.append(descendant)
		return descendants
	
	def remove_duplicates(self, obj, cur, count=0):
		if count >= 2:
			for child in cur.children:
				if child == obj:
					cur.children.remove(child)	
					child.parents.remove(cur)
					break
		for parent in cur.parents:
			self.remove_duplicates(obj, parent, count + 1)
	
	def is_descendant(self, descendant, ancester):
		if descendant == ancester:
			return True
		for child in ancester.children:
			if self.is_descendant(descendant, child):
				return True
		return False

	def find_act(self, obj, act):
		address = None
		for action in obj.actions:
			address = find_act2(action, act)
			if address != None:
				break

	def find_act2(self, cur, act):
		if cur.word == "|||": # end
			if act == []:
				return cur.parent	
			else:
				return None
		address = None
		if cur.word == act[0]:
			for child in cur.children:
				address = find_act2(child, act[1:])
				if address != None:
					break
				
					
		

	def find_obj(self, word):
		return self.find_word(word, self.objects)	

	def find_word(self, word, objects, start = 0, end = None):
		if end == None:
			end = len(objects) - 1
		
		if start > end:
			return None
		
		mid = (start + end) / 2
		rel = self.compare_word(word, objects[mid].word)
		if rel == -1:
			return self.find_word(word, objects, start, mid - 1)
		elif rel == 1:
			return self.find_word(word, objects, mid + 1, end)
		else:
			return objects[mid]
	
	def insert_obj(self, obj):
		self.insert_word(obj, self.objects)

	def insert_word(self, obj, objects):
		index = 0
		while index < len(objects) and self.compare_word(obj.word, objects[index].word) >= 0:
			index += 1
		objects.insert(index, obj)
	
	def compare_word(self, a, b):
		
		i = 0
		while i < len(a) and i < len(b) and a[i] == b[i]:	
			i += 1			
		if i >= len(a) or i >= len(b):
			i -= 1
		
		if a[i] == b[i]:
			if len(a) < len(b):
				return -1
			elif len(a) > len(b):
				return 1
			else:
				return 0
		elif ord(a[i]) < ord(b[i]):
			return -1
		else:
			return 1
