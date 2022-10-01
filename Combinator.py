from time import time, time_ns, sleep, strftime
from typing import List
import os
import multiprocessing as mp
import math

class Combinator(object):
	# Combinator specific
	maxDepth = 1
	wordlist = []

	# Stats
	wordsCreated = 0
	timeNeeded = 0
	
	# Parallel processing
	paralellSetupDone = False
	coresToUse = 1
	wordlistLength = 0
	chunkSize = 0
	mergeFiles = False
	launchedByGo = False
	outFileNames = []
	outFileHandles = []
	processStatus = []

	# Output specific
	debug = False
	outputToPrint = True
	outputToFile = False
	outputToList = False
	outFileName = None
	outFileHandle = None
	outputList = []
	
	# Benchmark specifics
	benchmarkWordlist = ['This', 'Wordlist', 'Has', 'Twelve', 'Unique', 'Entries', 'And' 'Is', 'Used', 'To', 'Create', 'Benchmarks']
	runBenchmark = False
	printTime = 0.000125
	writeTime = 0.000008382930183

	# ============================ CONSTRUCTOR ============================ #
	def __init__(self, wordlist, maxDepth:int = 1, *args, **kwargs):
		self.set_wordlist(wordlist)
		self.set_max_depth(maxDepth)
		self.launchedByGo = False
		pass


	# ============================ SETTER ============================ #
	def set_wordlist(self, wordlist ):
		if len(wordlist) > 0:
			self.wordlist = wordlist
			self.wordlistLength = len(wordlist)
			self.chunkSize = self.wordlistLength

	def set_max_depth(self, maxDepth:int ):
		if maxDepth > 0:
			self.maxDepth = maxDepth


	def enable_output_to_print(self):
		self.outputToPrint = True

	def enable_output_to_file(self, outFile:str ):
		self.outFileName = outFile
		self.outputToFile = True
	
	def enable_output_to_list(self):
		self.outputToList = True

	def disable_output_to_print(self):
		self.outputToPrint = False

	def disable_output_to_file(self):
		self.outputToFile = False

	def disable_output_to_list(self):
		self.outputToList = False

	# ============================ GETTER ============================ #

	def get_words_created(self) -> int:
		return self.wordsCreated

	def get_time_needed(self) -> float:
		return self.timeNeeded


	# ============================ BENCHMARK ============================ #
	def estimate_runtime(self, doBenchmark: bool=False) -> float:
		printTimePerEntry = 0
		writeTimePerEntry = 0

		# Calculate durations per entry
		calculationTimePerEntry = self.__benchmark_calculation(5)
		
		if self.outputToPrint:
			if doBenchmark:
				printTimePerEntry = self.__benchmark_print()
			else:
				printTimePerEntry = self.printTime

		if self.outputToFile:
			if doBenchmark:
				writeTimePerEntry = self.__benchmark_file()
			else:
				writeTimePerEntry = self.writeTime

		estimatedEntries = self.pow_sum(len(self.wordlist), self.maxDepth)
		estimatedDuration = (estimatedEntries * (calculationTimePerEntry + printTimePerEntry + writeTimePerEntry )) / self.coresToUse
		return estimatedDuration

	def __benchmark_calculation(self, depth:int) -> float:
		
		# Load benchmark-configuration
		originalWordlist = self.wordlist
		originalMaxDepth = self.maxDepth
		originalCoresToUse = self.coresToUse
		self.set_wordlist(self.benchmarkWordlist)
		self.maxDepth = depth
		self.disable_parallel_processing()

		self.runBenchmark = True
		self.go()
		self.runBenchmark = False

		# Return original configuration
		self.set_wordlist(originalWordlist)
		self.maxDepth = originalMaxDepth
		self.enable_parallel_processing(originalCoresToUse)

		return (self.timeNeeded / self.wordsCreated)/originalCoresToUse

	def __benchmark_print(self, rows:int=250) -> float:
		conversionFactor = 1000000000
		b_start = time_ns()
		for i in range(0, rows):
			print(f"Print benchmark in Progres: Row {i+1} / {rows} ", flush=True)
		b_end = time_ns()
		costPerLine = (((b_end - b_start) / rows) / conversionFactor)
		self.printTime = costPerLine
		return costPerLine

	def __benchmark_file(self, rows:int=250) -> float:
		conversionFactor = 1000000000
		fileName = "benchmark_" + strftime("%Y-%m-%d_%H-%M-%S") + ".tmp"
		fileHandle = open(fileName, "w")

		b_start = time_ns()
		for i in range(0, rows):
			fileHandle.write(f"Print benchmark in Progres: Row {i+1} / {rows} ")
		b_end = time_ns()

		fileHandle.close()
		if os.path.isfile(fileName):
			os.remove(fileName)

		costPerLine = (((b_end - b_start) / rows) / conversionFactor)
		self.writeTime = costPerLine
		return costPerLine

	# ============================ COMBINATION ============================ #

	def createToPrint(self):
		self.enable_output_to_print()
		self.disable_output_to_file()
		self.disable_output_to_list()
		return self.go()

	def createToFile(self, outFile:str ):
		self.enable_output_to_file(outFile)
		self.disable_output_to_list()
		self.disable_output_to_print()
		return self.go()

	def createToList(self):
		self.disable_output_to_print()
		self.disable_output_to_file()
		self.enable_output_to_list()
		return self.go()


	def go(self):
		self.wordsCreated = 0
		self.timeNeeded = 0
		self.launchedByGo = True
		outputStart = time()

		if self.outputToList:
			self.outputList = []

		if len(self.wordlist) > 0:
			self.__launch_parallel()
		
		outputEnd = time()
		self.timeNeeded = (outputEnd - outputStart)
		self.launchedByGo = False

		return self.outputList


	# ============================ PARALLEL ============================ #

	def enable_parallel_processing( self, coresToUse:int=0 ):
		if coresToUse >= 0:
			maxCores = mp.cpu_count()
			if coresToUse > maxCores or coresToUse == 0:
				coresToUse = maxCores
			self.coresToUse = coresToUse
			self.chunkSize = math.ceil(self.wordlistLength / coresToUse)
			self.outFileNames = [None] * coresToUse
			self.processStatus = [None] * coresToUse
			self.outFileHandles = [None] * coresToUse

	def disable_parallel_processing(self):
		self.enable_parallel_processing(1)

	def __launch_parallel(self):
		if self.coresToUse > 1:
			processes = []
			for i in range(0, self.coresToUse):
				if self.debug: 
					print(f"Spawning process {i}/{self.coresToUse}")
				self.processStatus[i] = "spawned"
				p = mp.Process(target=self.parallel_fetch_from_list, args=(i,))
				processes.append(p)

			[x.start() for x in processes]
		else:
			if self.debug: 
				print("Using Single Process")
			self.parallel_fetch_from_list(0)

	def parallel_fetch_from_list(self, core:int=0):
		# prevent uninitialized paralell runs
		if not self.launchedByGo:
			self.disable_parallel_processing()
			core=0

		self.processStatus[core] = "started"

		# Calculate range
		fromLine = (core * self.chunkSize)
		toLine = (fromLine + self.chunkSize)
		if toLine > self.wordlistLength:
			toLine = self.wordlistLength

		if fromLine < toLine:
			if self.debug:
				print(f"Fetching lines {fromLine} to {toLine}")
			# prepare file
			if self.outputToFile and not self.runBenchmark:
				if self.coresToUse == 1:
					self.outFileHandle = open(self.outFileName, "w")
				else:
					subFileName = self.outFileName + ".t" + str(core)
					self.outFileNames[core] = subFileName
					self.outFileHandles[core] = open(subFileName, "w")

			# start processing
			self.processStatus[core] = "running"
			for i in range(fromLine, toLine):
				self.__parallel_combine(self.wordlist[i], core)

		# finish up
		if self.outFileHandles[core]:
			self.outFileHandles[core].close()
		self.processStatus[core] = "done"

	def __parallel_combine(self, base:str, core:int=0, depth:int=1):
		self.__parallel_output(base, core)
		if depth < self.maxDepth:
			for word in self.wordlist:
				self.__parallel_combine((base+word), core, (depth+1))

	def __parallel_output(self, word:str, core:int=0):
		self.wordsCreated += 1
		if not self.runBenchmark:
			if self.outputToFile:
				if self.coresToUse == 1:
					self.outFileHandle.write(word+"\n")
				else:
					self.outFileHandles[core].write(word+"\n")
			if self.outputToPrint:
				print(word, flush=True)
			if self.outputToList:
				self.outputList.append(word)

	def __merge_files(self):
		with open(self.outFileName, "w") as outFile:
			for tempFile in self.outFileNames:
				with open(tempFile) as inFile:
					for line in inFile:
						outFile.write(line+"\n")


	# ============================ HELPER ============================ #

	@staticmethod
	def pow_sum (base: int, maxExponent: int) -> int:
		total = 0
		for i in range(1, maxExponent+1):
			total+=pow(base, i)
		return total

	# formats input in the form of "seconds,milliseconds" into human readable strings
	@staticmethod
	def format_time(duration:float ) -> str:

		# setup knowledge
		milliSecondsInASecond = 1000
		secondsInAMinute = 60
		minutesInAHour = 60
		hoursInADay = 24

		# stats
		milliseconds = 0
		seconds = 0
		minutes = 0
		hours = 0
		days = 0

		# seconds and milliseconds
		seconds = duration // 1
		milliseconds = (duration - seconds) * milliSecondsInASecond

		# minutes
		if seconds >= secondsInAMinute:
			minutes = seconds // secondsInAMinute
			seconds = seconds % secondsInAMinute

		# hours
		if minutes >= minutesInAHour:
			hours = minutes // minutesInAHour
			minutes = seconds % minutesInAHour

		# days
		if hours >= hoursInADay:
			days = hours // hoursInADay
			hours = hours % hoursInADay

		# create output
		result = '' + str(int(seconds)) + "s " + str(int(milliseconds)) + "ms"

		if minutes > 0 or hours > 0 or days > 0:
			result = '' + str(int(minutes)) + "m " + result
			if hours > 0 or days > 0:
				result = '' + str(int(hours)) + "h " + result
				if days > 0:
					result = '' + str(int(days)) + "d " + result

		return result