
#Mersenne Twister MT 19937
class MT19937:
	def __init__(self, seed):
		self.MT = [0] * 624
		self.index = 0
		self.MT[0] = seed 
		for i in range(1, 624):
			self.MT[i] = 0xFFFFFFFF & (1812433253 * (self.MT[i - 1] ^ self.MT[i - 1] >> 30) + i)

	#Extract a tempered value based on MT[index]
	#calling twist() every n numbers
	def extract_number(self):
		if self.index == 0:
			self.generate_numbers()
        
		y = self.MT[self.index]
		y ^= y >> 11
		y ^= (y << 7) & 0x9D2C5680
		y ^= (y << 15) & 0xEFC60000
		y ^= y >> 18

		self.index = (self.index + 1) % 624
		return y

	def generate_numbers(self):
		for i in range(624):
			y = (self.MT[i] & 0x80000000) + (self.MT[(i + 1) % 624] & 0x7FFFFFFF)
			self.MT[i] = self.MT[(i + 397) % 624] ^ y >> 1
			if y % 2 != 0:
				self.MT[i] ^= 0x9908B0DF

	#Generate the next n values from the series x_i 
	def twist(self):
		#TODO: Mix state here
		return

	def unmix(self, y):
		y ^= y >> 18

		y ^= (y << 15) & 0xEFC60000

		for _ in range(7):
			y ^= (y << 7) & 0x9D2C5680

		for _ in range(11):
			y ^= y >> 11

		return y

