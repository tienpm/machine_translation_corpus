import nltk
import underthesea


class EnToolkit:
	def __init__(self):
		self.grammar = "NP: {<DT>?<JJ>*<NN>}"

	def word_seg(self, sentence):
		return nltk.word_tokenize(sentence)

	def pos_tagging(self, tokens):
		return nltk.pos_tag(tokens)

	def chunking(self, tags, grammar=None):
		if grammar is None:
			grammar = self.grammar
		cp = nltk.RegexpParser(grammar)
		return cp.parse(tags)

class ViToolkit:
	def __init__(self):
		pass

	def word_seg(self, sentence):
		return underthesea.word_tokenize(sentence)

	def pos_tagging(self, tokens):
		return underthesea.pos_tag(tokens) 

	def chunking(self, tags):
		return underthesea.chunk(tags)