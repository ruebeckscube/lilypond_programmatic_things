#!/usr/local/bin/python3

import logicUI
import argparse
import os

parser = argparse.ArgumentParser(description="Imports the specified midi file to the active Logic project at the beginning of the Cycle range.")
parser.add_argument("num_tracks", type=int, help="The number of tracks in the midi file.")
parser.add_argument("file_name", type=str, help="Absolute location of the file. Changes extension to .midi")
parser.add_argument("--first", action="store_true", help="IMPORTANT: Add this flag if it's the first time you're running this on the logic file, or if you've deleted all the midi tracks.")

args = parser.parse_args()
file_name = os.path.splitext(args.file_name)[0] + ".midi"
num_tracks = args.num_tracks
is_first = args.first

logic = logicUI.LogicUI()
logic.toggleMixerOnOff()
logic.goToLeftLocator()
logic.importMidi(file_name)
if not is_first:
    logic.move_last_tracks_to_prev_tracks(num_tracks)
logic.goToLeftLocator()
