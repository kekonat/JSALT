class Pair(object):

	def __init__(self, yomi):
		self.dict = {yomi : 1}
		
	def make_pair(yomi):
		pair = Pair(yomi)
		return pair
		
	def add_count(self, yomi):
		if yomi in self.dict:
			self.dict[yomi] += 1
		else:
			self.dict[yomi] = 1
			
	def get_dict(self):
		return self.dict
			
	def merge(self, pair):
		for k, v in pair.get_dict().iteritems():
			if k in self.dict:
				self.dict[k] = self.dict[k] + v
			else:
				self.dict[k] = v
		return self
		
	