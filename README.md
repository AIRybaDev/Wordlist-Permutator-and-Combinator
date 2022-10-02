# Recursive Permutation and Combination Generator


## Table of contents
- [Recursive Permutation and Combination Generator](#recursive-permutation-and-combination-generator)
	- [Table of contents](#table-of-contents)
	- [Preface](#preface)
	- [What this program does](#what-this-program-does)
	- [How this program works](#how-this-program-works)
	- [Options](#options)
	- [Permutations](#permutations)
	- [Recombinations](#recombinations)
	- [Multithreading](#multithreading)

## Preface
As this project is the result of my first dabbling with python3, there are without any shadow of doubt that things could be improved or generally "done better" than I have. Feel free to fork and later submit a merge request if you see something that can be further optimized.

## What this program does
This program is meant to generate extensive wordlists by recursively permutating and combining different fragments that have been passed to it in a file and/or via a pipe and outputting this worldist either into STDOUT or a file.

This is meant for situations, where one cannot remember a specific password entirely, but has some guesses about which fragments could ahve possibly been included in the password. This porgram then generates possible password-candidates based on the passed fragments and chosen level of permutation and recombination-depth. 

## How this program works
1. A list of fragments is passed to this program
2. All permutations of any word in the list of fragments for a given permutation level are added to the list of fragments
3. All words within this new list of fragments are combined with all other words in this list up to the depth chosen by the user
4. The resulting list is either printed to STDOUT or written into a file

## Options

| Shorthand     | Long Version          | Parameter                                        | Effect                                                                                                                                                                                               |
| ------------- | --------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-i "<FILE>"` | `--infile "<FILE>"`   | The file to read fragments from                  | Adds all Fragments contained in 'FILE' to the list of fragments to use                                                                                                                               |
| `-o "FILE"`   | `--outfile "FILE"`    | The path and Filename fpr the resulting wordlist | Stores the generated wordlist under 'FILE'. If omitted, the wordlist is instead redirected to STDOUT.                                                                                                |
| `-p [0-4]`    | `--permutation [0-4]` | The desired level of permutations                | See Section [Permutations](#Permutations).                                                                                                                                                           |
| `-d <INT>`    | `--depth <INT>`       | The desired depth of recombinations              | See Section [Recombinations](#Recombinations).                                                                                                                                                       |
| `-v`          | `--verbose`           | none                                             | Enables verbose output. Requires eitther -e or -o                                                                                                                                                    |
| `-e`          | `--estimate`          | none                                             | Calculate the estimated duration to calculate the given list with the given parameters. Since this mode first benchmarks the system, the process might take a moment. Automatically enables -v Flag. |
| `-H <INT>`    | `--hashes <INT>`      | Hashes per seconds                               | Hashes per second used for the estimated duration of actually using the generated wordlist against any specific hash. If omitted, no duration for hashing will be computed.                          |
| `-c <INT>`    | `--cores <INT>`       | The number of cores to use                       | Enables multithreading. Default: 1. See Section [Multithreading](#Multithreading) for more info.                                                                                                     |

## Permutations
In regards to the possible permutations of a given word that this program can produce, there are four levels the user can choose, with each one including the permutations of the previous level.

The permutation level can be set via `-p [0-4]` in the command line, with the default being a permutation level 0 (so no permutations whatsoever).

**Level 0:** Just the word as it is
* foo

**Level 1:** "Full lowercase" and "First Char Uppercase"
All of level 0 plus:
* Foo

**Level 2:** "Full Uppercase" and "Wobblecase"
All of level 1 plus:
* FOO
* fOo
* FoO

**Level 3:** Every case-variation possible
All of level 2 plus:
* fOo
* foO
* FOo
* fOO

**Level 4:** Every 1337-speak variation of every case-variation possible
All of level 3 plus:
* f0o
* F0o
* f0O
* F0O
* fo0
* Fo0
* fO0
* FO0
* f00
* F00

The `Permutator.py` class allows the user to enable the differnet kinds of permutations individually, but `main.py` groups it into the four levels described above to make usage more straightforward.

Keep in mind though that Levels 3 and 4 will increase the size of fragment-list exponentially, which snowballs further with a higher recombination depth. This means that even a list of less than 20 fragments can produce a wordlist that is hundrets of gigabytes in size. To calculate the amount of words in the resulting wordlist and therefore get an implicit estimate of the resulting filesize, use the `-e` flag together with your input parameters. 

## Recombinations
The recombination of the fragment-list is being handled by the `Combinator.py` class, which requires a list of fragments to (re-)combine as well as the depth of the recombination, i.e. up to how many fragments are combined into one word for the resulting wordlist.

Assuming, we have a fragment-list containing only "foo" and "bar", these would be the results:

**Depth 1:**
* foo
* bar

**Depth 2:**
* foo
* bar
* foofoo
* foobar
* barfoo
* barbar

**Depth 3:**
* foo
* bar
* foofoo
* foobar
* barfoo
* barbar
* foofoofoo
* foofoobar
* foobarfoo
* barfoofoo
* foobarbar
* barbarfoo
* barfoobar
* barbarbar

## Multithreading
To make the generation of the resulting wordlist at least a bit more time-efficient, this tool features a rudimentary method of multithreading the workload, thus greatly reducing the reqiured time to calculate the wordlist if a sufficient number of cores is available.

Currently, only the recombination part of this tool is able to process the fragment-list in parallel. This is achieved by starting each thread on a different point on the in itial fragment-list and having it only process 1/nth of the entries in the initial fragment-list. This also means that some threads may finish their work faster than others due to having less words to process. To accomodate for this, every thread writes its output in a separate part-file with the `.t<NUMBER>` extension, where `NUMBER` represents the core-number on  which the file was being processed.

This whiole process is not ideal, but achieves the intended result. In a future update, these files could be merged automatically once the pocessing is done.