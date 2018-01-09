from helpers import *

# This class will contain links to information about itself as well as
# how it relates to other objects in the form of a dependency tree.
class Object:

	def __init__(self):
	
		# the two forms of the word describing this object	
		self.name = ""
	
		# objects directly related to this one
		self.parents = []
		self.children = []

		# all data referencing this object	
		self.data = []

# This class will provide methods to load and save all the information
# that the program goes through.  It will also be used for deleting
# unnecessary information as well.
class Memory:

	def __init__(self, data_file, tree_file):

		self.objects = []
		self.tree = None	

	def add_data(self, data):
	
		# adds statement to data	
		self.data.append([data, "heard"])

		words = data.split()
		for word in words:
			found = False
			for object in self.objects:
				if object.name == word:
					found = True
					object.data.append(len(self.data))
					break
				
			
	
class Tree:

	def __init__(self, file_name=None):

		self.file_name = file_name
		self.roots = [] 
		if file_name != None:
			self.load_tree()

	def load_tree(self):
		
		file = open(self.file_name, 'r')
		curr = None
		lines = file.readlines()
		file.close()
		for line in lines:
			line = line.split('\n')
	
		index = 0
		while index < len(lines):
			line = lines[index].split('|')		
			name = line[0]
			size = int(line[1])
			node = Node(name)

			if size == 0:
				pass

			else:	

				for i in range(0, size):
					index += 1
					[child, index] = self.load_node(lines, index)
					node.add_child(child)
			self.roots.append(node)
			index += 1

	def load_node(self, lines, index):
		line = lines[index].split('|')		
		name = line[0]
		size = int(line[1])
		node = Node(name)

		if size == 0:
			pass

		else:	
	
			for i in range(0, size):
				index += 1
				[child, index] = self.load_node(lines, index)
				node.add_child(child)

		return [node, index]

	def save(self):
		txt = ""
		for root in self.roots:
			txt = txt + root.to_str()
		file = open(self.file_name, 'w')
		file.write(txt)
		file.close()

	# adds a sentence to the tree 
	def add_sen(self, sen):
		if len(sen) == 0:
			return
		for root in self.roots:
			if sen[0] == root.word:
				root.add_sen(sen[1:])
				return
		self.roots.append(Node(sen[0]))
		curr = self.roots[-1]
		for word in sen[1:]:
			curr.children.append(Node(word))
			curr = curr.children[0]	

	# adds a file of text to the tree
	def add_html_file(self, file_name):
		file = open(file_name, 'r')
		org_txt = file.read()
		sen = ""
		in_tag = False
		for c in org_txt:
			if c == '<':
				in_tag = True
				sen = ""
			elif c == '>':
				in_tag = False
				sen = ""
			else:
				if not in_tag:
					sen = sen + c	
					if c in ['.', '?', '!']:
						
						words = sen.lower().split()
						words = sep_punc(words)
						try:
							self.add_sen(words)
						except:
							print sen
						sen = ""
				

class Node:
	
	def __init__(self, word):
		
		self.word = word		
		self.children = []

	def add_child(self, node):
		self.children.append(node)

	def to_str(self):
		
		txt = self.word + "|" + str(len(self.children)) + "\n"
		for child in self.children:
			txt = txt + child.to_str()
			
		return txt 

	def add_sen(self, sen):
		if len(sen) == 0:
			return
		for child in self.children:
			if sen[0] == child.word:
				child.add_sen(sen[1:])
				return

		self.children.append(Node(sen[0]))
		curr = self.children[-1]
		for word in sen[1:]:
			curr.children.append(Node(word))
			curr = curr.children[0]	

			
		
			






