from typing import List

class Permutator:
	lowercase = True
	uppercase = True
	firstUpper = True
	wobbleCase = False
	leetspeak = False
	allCase = False

	# ===================  CONSTRUCTOR  =================== #
	def __init__(self, lowercase:bool=True, uppercase:bool=True, firstUpper:bool=True, wobbleCase:bool=False, leetspeak:bool=False, allCase:bool=False ):
		self.set_lowercase(lowercase)
		self.set_uppercase(uppercase)
		self.set_first_upper(firstUpper)
		self.set_wobblecase(wobbleCase)
		self.set_leetspeak(leetspeak)
		self.set_all_case_variations(allCase)


	# ===================  SETUP  =================== #
	
	# lowercase
	def enable_lowercase(self):
		self.set_lowercase(True)

	def disable_lowercase(self):
		self.set_lowercase(False)
	
	def set_lowercase(self, mode:bool):
		self.lowercase = mode


	# UPPERCASE
	def enable_uppercase(self):
		self.set_uppercase(True)

	def disable_uppercase(self):
		self.set_uppercase(False)
	
	def set_uppercase(self, mode:bool):
		self.uppercase = mode


	# Firstupper
	def enable_first_upper(self):
		self.set_first_upper(True)

	def disable_first_upper(self):
		self.set_first_upper(False)
	
	def set_first_upper(self, mode:bool):
		self.firstUpper = mode


	# WoBbLeCaSe
	def enable_wobblecase(self):
		self.set_wobblecase(True)

	def disable_wobblecase(self):
		self.set_wobblecase(False)
	
	def set_wobblecase(self, mode:bool):
		self.wobbleCase = mode


	# 1337speak
	def enable_leetspeak(self):
		self.set_leetspeak(True)

	def disable_leetspeak(self):
		self.set_leetspeak(False)
	
	def set_leetspeak(self, mode:bool):
		self.leetspeak = mode


	# ALL THE COMBINATIONS! (╯°□°)╯︵ ┻━┻
	def enable_all_case_variations(self):
		self.set_all_case_variations(True)

	def disable_all_case_variations(self):
		self.set_all_case_variations(False)
	
	def set_all_case_variations(self, mode:bool):
		self.allCase = mode



	# ===================  USAGE  =================== #

	# the permute-method offers the same boolean-Switches to activate or deactivate different permutations as the constructor. This is a deliberate choice to make the class more flexible: A object of this class can be created with one default-configuration but overridden to a different configuration without the need to create a second object of this class.
	def permute( self, input:str, lowercase:bool=None, uppercase:bool=None, firstUpper:bool=None, wobbleCase:bool=None, leetspeak:bool=None, allCase:bool=None ) -> List[str]:
		result = []
		result.append(input)

		if self.__bool_override( self.allCase, allCase ):
			result = self.case_variations( input )
			if self.__bool_override( self.leetspeak, leetspeak ):
				for leet in self.leet_variations( input ):
					result = result + self.case_variations( leet )
		else:
			if self.__bool_override( self.lowercase, lowercase ):
				result.append(input.lower())

			if self.__bool_override( self.uppercase, uppercase ):
				result.append(input.upper())

			if self.__bool_override( self.firstUpper, firstUpper ):
				result.append(input.capitalize())

			if self.__bool_override( self.wobbleCase, wobbleCase ):
				buffer = self.wobble_case( input )
				result.append(buffer)
				result.append(self.invert_case(buffer))

			if self.__bool_override( self.leetspeak, leetspeak ):
				result = result + self.leet_variations( input )

		return list(set(result))



	# ===================  CONVERTER  =================== #

	# inverts the case for every letter of the given input
	@staticmethod
	def invert_case( input: str ) -> str:
		output = []
		for c in input:
			if c.isupper():
				output.append(c.lower())
			elif c.islower():
				output.append(c.upper())
			else:
				output.append(c)
		return ''.join(output)

	# converts the given input into alternating upper- and lowercase letters
	@staticmethod
	def wobble_case( input: str ) -> str:
		output = []
		ctr = 0
		input = input.lower()
		for c in input:
			if ctr % 2:
				output.append(c.upper())
			else:
				output.append(c.lower())
			ctr+=1
		return ''.join(output)

	# creates evey possible combination of upper- and lowercase for each char in the given input
	@staticmethod
	def case_variations( input: str, filter: bool=True ) -> List[str]:
		result = []
		if len(input) == 1:
			result.append(input.upper())
			result.append(input.lower())
		else:
			c = input[0]
			for variant in Permutator.case_variations(input[1:], False):
				result.append( c.upper() + variant )
				result.append( c.lower() + variant )
		if filter:
			result = list(set(result))

		return result

	# creates every possible 1337speak-variant of the given input
	@staticmethod
	def leet_variations (input: str, filter: bool=True ) -> List[str]:
		result = []
		
		LeetMap = dict()
		LeetMap['a'] = ['4', '@', '^']
		LeetMap['b'] = ['8']
		LeetMap['c'] = ['(']
		LeetMap['e'] = ['3', '€']
		LeetMap['g'] = ['6', '9']
		LeetMap['h'] = ['#', '4']
		LeetMap['i'] = ['1', '!', '|']
		LeetMap['l'] = ['1', '|']
		LeetMap['o'] = ['0']
		LeetMap['s'] = ['5', '$', '§']
		LeetMap['t'] = ['1', '7']
		LeetMap['z'] = ['2']

		if len(input) == 1:
			if input.lower() in LeetMap:
				result = LeetMap[input.lower()]
			result.append(input)
		else:
			c = input[0]
			c = c.lower()
			for variant in Permutator.leet_variations(input[1:], False):
				if c in LeetMap:
					for leet in LeetMap[c]:
						result.append( leet + variant )
				result.append( c + variant )
		if filter:
			result = list(set(result))

		return result


	# ===================  HELPER  =================== #

	@staticmethod
	def __bool_override( default:bool, custom:bool = None):
		if custom is None:
			return default
		else:
			return custom
