# Lilypond programmatic stuff

This is a set of examples of some of the ways I've interacted with Lilypond
programmatically (via mostly python).

## Semi-random piece composition
Files:

- joe.py (the script to generate the piece)
- joepiece1.ly (the resulting piece of music from that script, in Lilypond)
- joepiece1.pdf (a pdf of that piece)

This was a project from college right after our professor introduced us to Lilypond,
where my classmate Joe wanted to semi-randomly generate a piece. I forget exactly
the conception, but the comments in the python file should give a pretty good
sense of the compositional intention! In this case, the python file generates
Lilypond code that is then compiled into a pdf.

## Workflow with Logic
Files:

- logicUI.py (defines some functions for interacting with Logic via accessibility features)
- import_midi_to_logic.py (given a midi file, imports it into the open Logic session)
- emacs_config_example.el (defines an emacs function to call while editing a Lilypond file)

[Video demo in my reddit post](https://www.reddit.com/r/emacs/comments/zvsw4r/had_my_first_real_emacs_as_an_extensible_editor/)

The comment in the reddit post linked above describes the workflow I automated.
The python scripts in this case interact with the MIDI _output_ of Lilypond. The
emacs function acts on the currently open Lilypond file and offers some
interactive prompts, making the whole workflow quite smooth.
