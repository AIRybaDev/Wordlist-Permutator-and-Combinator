#!/usr/bin/env python

# ================================ IMPORTS ================================ #

import sys
import argparse
import os.path
from typing import List
from time import time

from Combinator import Combinator
from Permutator import Permutator


# ================================ FUNCTIONS ================================ #

# Credit to StackOverflow User "Wai Ha Lee"
# Based on an algorithm by Fred Cirera
# Source: https://stackoverflow.com/a/1094933
def sizeof_fmt(num, suffix='B'):
	for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, 'Yi', suffix)


# ================================ MAIN ================================ #

if __name__ == '__main__':
	# ================================ VARIABLES ================================ #

	# Allgemeinen Ziel-Array für alle Eingaben anlegen
	bucket = []
	wordlist = []
	liveOutput=False
	verbose=False
	fullBenchmark=True

	# Statistics
	totalLinesRead = 0
	uniqueLinesRead = 0
	permutationsCreated = 0
	expectedOutputSize = 0

	bytePerLine = 22.436

	# ================================ CLI PARAMETER ================================ #

	# Parser initialisieren
	parser = argparse.ArgumentParser(
		description=""" Permutation Generator 9000 """,
		formatter_class=argparse.RawDescriptionHelpFormatter,
	)

	# Argumente definieren
	parser.add_argument(
		"-i",
		action="store",
		dest="infile",
		default=None,
		help=" Path to the input file",
	)

	parser.add_argument(
		"-o",
		action="store",
		dest="outfile",
		default=None,
		help="Saves the created wordlist into OUTFILE. If omitted, the created wordlist will be sent to STDOUT instead.",
	)

	parser.add_argument(
		"-p",
		action="store",
		dest="permutation",
		choices=[0, 1, 2, 3, 4],
		default="none",
		type=int,
		help="""Select the Level of Permuations to apply:
				(Every level contains all the permutations before it)
				0: no Permutations at all (default)
				| 1: full lowercase, first char upper
				| 2: full uppercase, WoBbLeCaSe
				| 3: every case-variation possible
				| 4: every 1337speak variation possible
		""",
	)

	parser.add_argument(
		"-d",
		action="store",
		dest="depth",
		type=int,
		default=2,
		help="Create all possible combinations with DEPTH words. (Default: 2)",
	)

	parser.add_argument(
		"-v",
		action="store_true",
		dest="verbose",
		help="Enable verbose output (requires -o or -e)",
	)

	parser.add_argument(
		"-e",
		action="store_true",
		dest="estimate",
		help="Calculate the estimated duration to calculate the given list with the given parameters. Since this mode first benchmarks the system, the process might take a moment. Automatically enables -v Flag.",
	)

	parser.add_argument(
		"-H",
		action="store",
		dest="hashes",
		type=int,
		default=None,
		help="Hashes per second for -e",
	)

	parser.add_argument(
		"-c",
		action="store",
		dest="cores",
		default=1,
		type=int,
		help="Number of cores to use",
	)


	# Argumente abfragen
	args = parser.parse_args()


	# ================================ DATA IMPORT ================================ #

	# Wörter aus Datei importieren
	if args.infile:
		if os.path.isfile(args.infile):
			for line in open(args.infile, 'r', encoding='utf-8'):
				line = line.strip()
				bucket.append(line)
		else:
			parser.print_help()
			print("\nerror: File invalid or nonexistent.")
			exit()


	# Wörter aus Stdin (pipe) lesen
	if not sys.stdin.isatty(): 
		for line in sys.stdin: 
			line = line.strip()
			bucket.append(line)


	# ================================ CHECKS ================================ #

	if not bucket:
		parser.print_help()
		print("\nerror: No wordlist passed.")
		exit()

	if args.verbose:
		verbose = True

	if not args.outfile:
		liveOutput = True

	if args.estimate:
		verbose = True
		liveOutput = False

	# ================================ PREPARATION ================================ #

	# Initilaize Permutator Class
	permutator = Permutator((args.permutation > 0), (args.permutation > 1), (args.permutation > 0), (args.permutation > 1), (args.permutation > 3), (args.permutation > 2))


	# count before filtering
	totalLinesRead = len(bucket)

	# Filter for Unique entries 
	bucket = list(set(bucket))

	# count after filtering
	uniqueLinesRead = len(bucket)

	if verbose:
		print()
		print(f"Permutation Level: {args.permutation}")
		print(f"Depth: {args.depth}")
		print()
		print(f"Total lines read:  {totalLinesRead:,}")
		print(f"Unique lines read: {uniqueLinesRead:,}")
		if args.permutation > 0:
			print()
			print("Creating permutations, please wait...")

	bucketStart = time()

	# Copy bucket and create permutations
	for word in bucket:
		wordlist = wordlist + permutator.permute( word )

	bucketStop = time()

	# free ram
	del bucket

	# Filter for Unique entries again
	wordlist = list(set(wordlist))

	# Initilaize Combinator Class
	combinator = Combinator(wordlist, args.depth)

	if args.outfile:
		combinator.enable_output_to_file(args.outfile)
		combinator.disable_output_to_print()
	else:
		combinator.enable_output_to_print()

	if args.cores >= 0:
		combinator.enable_parallel_processing(args.cores) 

	# create more stats
	permutationsCreated = len(wordlist)
	expectedOutputSize = combinator.pow_sum(len(wordlist), args.depth)


	if verbose:
		if args.permutation > 0:
			print( f"Created {(permutationsCreated - uniqueLinesRead):,} additional words in " + combinator.format_time((bucketStop - bucketStart)) )
		print()
		print( f"Total wordlist contains {permutationsCreated:,} entries.")
		print( f"Expected result will have appx. {expectedOutputSize:,} entries." )



	# ================================ MAIN ================================ #

	if not args.estimate:
		result = combinator.go()

		if verbose:
			print()
			print(f"Created {combinator.get_words_created():,} Entries in " + combinator.format_time(combinator.get_time_needed()) )
	else:
		# Just benchmark
		print()
		print("Starting Benchmark, please wait as this might take a while")

		creationDuration = combinator.estimate_runtime(fullBenchmark)
		estimatedDuration = creationDuration + (bucketStop - bucketStart) 

		print()
		print("Estimated duration for creation: " + combinator.format_time(estimatedDuration) + f" for {expectedOutputSize:,} entries.")

		if args.outfile:
			estimatedFilesize = expectedOutputSize * bytePerLine
			print("Estimated filesize: " + sizeof_fmt(estimatedFilesize))

		if args.hashes:
			hashDuration = expectedOutputSize / args.hashes
			print("Estimated duration for hashing: " + combinator.format_time(hashDuration) + f" at {args.hashes / 1000:.3} k Hashes/second")

		print()