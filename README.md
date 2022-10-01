# Recursive Permutation and Combination Generator

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

In order to 

## Permutations
In regards to the possible permutations of a given word that this program can produce, there are four levels the user can choose, with each one including the permutations of the previous level.

**Level 0:** Just the word as it is
* foo

**Level 1:** "Full lowercase" and "First Char Uppercase"
* Foo

**Level 2:** "Full Uppercase" and "Wobblecase"
* FOO
* fOo
* FoO

**Level 3:** Every case-variation possible
* fOo
* foO
* FOo
* fOO

**Level 4:** Every 1337-speak variation of every case-variation possible
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

Keep in mind though that Levels 3 and 4 will exponentially increase the size of 

## 