###########################
## Concept by Joe Lowry
## Code by Joshua Ruebeck
## Jan. 19, 2015
############################


import random

def main():
	# Sets the maximum length a phrase can be
	MAX_PHRASE_LENGTH = 5

	# List of possible notes, will get shorter
	rightNotes = ["c'8","cs'8","d'8","ds'8","e'8","f'8","fs'8","g'8","gs'8","a'8","as'8","b'8","c''8"]
	leftNotes = ["c8","cs8","d8","ds8","e8","f8","fs8","g8","gs8","a8","as8","b8","c'8"]

	# The string that will hold the series of 8th notes for each hand
	rightLine = ""
	leftLine = ""

	# Determines the length of each of the 13 phrases
	phraseLengths = []
	for i in range(13):
		phraseLengths.append(random.randrange(1, MAX_PHRASE_LENGTH+1))
	
	# For each phrase, creates the appropriate number of measures of music by choosing random notes.
	# After each phrase, removes a note from the list of possible notes.
	for length in phraseLengths:
		for i in range(length):
			for j in range(8):
				rightLine = rightLine + rightNotes[random.randrange(0,len(rightNotes))] + " "
				leftLine = leftLine + leftNotes[random.randrange(0,len(leftNotes))] + " "
		rightNotes.pop(random.randrange(0,len(rightNotes)))
		leftNotes.pop(random.randrange(0,len(leftNotes)))

	# Generates the Lilypond code for the piece, to by copied from command line by user.
	lilyCode = '''
\\version "2.18.2"
\language english


\header {
	title = "Joe's Piece"
	composer = "Joe Lowry"
}
	\score {
	\\new StaffGroup <<
		\\time 4/4
		\\new Staff {
			''' + rightLine + '''
		}
		\\new Staff {
			\clef bass
			''' + leftLine + '''
		}
	>>

	\\layout { }
	\\midi { \\tempo 4 = 150 }
}
'''

	print lilyCode

main()