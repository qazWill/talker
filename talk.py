from helpers import *
from mem import *
from grammer import *

class Talker:

	def __init__(self, obj_file_name):

		self.memory = Memory(obj_file_name)
		self.log = []
		self.chain_id = ''
		self.chain_num = 0
		self.chain_set = False
		
	def close(self):
			
		self.memory.save()

	def chain(self, id):
		if not self.chain_set:
			self.chain_set = True 

			if id == self.chain_id:
				self.chain_num += 1
			else:
				self.chain_num = 1 
				self.chain_id = id

	def talk(self):

		# loops until done talking	
		input = " "
		while input not in ["bye", "good by", "see ya"]:
			
			input = raw_input("You >>> ")
			self.log.append(input)
			response = self.respond(input)
			print "\nBot >>> " + response + "\n"
			self.log.append(response)

	def respond(self, input):

		words = input.split()

		self.chain_set = False
		response = self.greet(input)	
		if response == "":
			response = self.what(input)
			if response == "":

				response = self.statement(input)
				if response == "":
					response = "Sorry, I'm confused."	
		self.chain("")
		return response

	def greet(self, input):
		if input in ["hi", "hello", "hey", "howdy"]:
			return input

		elif input in ["bye", "good by", "see ya"]:
			return "bye"
		
		return ""

	def what(self, input):
		response = "" # returned if not a what question
		words = sep_punc(input.split())
		if "what" in words:
			
			# the types of what sentences
			# what? 	*
			# what <noun with mods>    *
			# what <verb> <noun with mods> <verb end>     *
			# middle tell me what you like
			# suprise you are going to do what! or ?
			# mock you are going to defeat me with what?  your ___?

			# what? or what???  expression of suprise or confusion
			if len(words) == 2 and '?' in words[1] or words == ["what"]:
				if len(self.log) >= 2:
					response = "I said, " + self.log[-2]
					self.chain("what???")
					if self.chain_num == 2:
						response = "You know what I said..."
					elif self.chain_num == 3:
						response = "Please stop..."
					elif self.chain_num > 3:
						response = "..."
						
				else:
					response = 'What do you mean "what", we just started talking?!?!'
					
			# what is ______?
			if words[0] == "what" and (words[1] == "is" or words[1] == "are"):
		
				pass

	
			'''
			response = "I don't know"
			if words[1] in ["is", "are", "were", "was"]:
				str = ""
				for item in self.memory.data:
					words2 = item[0].split()
					words1 = []
					words1.append(words[2])
					words1.append(words[1])
					for i in range(3, len(words)):
						words1.append(words[i])
					if is_punc(words1[-1]):
						words1.pop()
					i = 0
					found = True 
					while i < len(words1) and i < len(words2):
						if words2[i] != words1[i]:
							found = False
							break
						i = i + 1
					if found:
						return item[0]
						
			'''							

		return response

			
			

	

	def statement(self, input):
		
		words = sep_punc(input.split())
		if words[0] == 'a' or words[0] == 'an':
			if words[2] == 'is':
				if words[3] == 'a' or words[3] == 'an':
					if len(words) == 5:
						self.memory.add_obj(words[1], words[4])
		return ""

		
	def test_func(self):
		self.test_func2()
		again = ""
		while again == "":
			label(raw_input(">>> "), self.memory)
			again = raw_input("again?")
			

	def test_func2(self):
	
		file = open("word_lists/adj1.txt", "r")
		for line in file.readlines():
			if line != "\n":
				word = line.split("\n")[0]		
				self.memory.add_adjective(word)	
		self.memory.add_noun("textbook")
		self.memory.add_verb(["confuse", "confuse", "confused", "confused"])
		self.memory.add_noun("me")
		self.memory.add_noun("city")
		self.memory.add_adjective("ripe")
		self.memory.add_adjective("red")
		self.memory.add_noun("this")

			

				

		


		
