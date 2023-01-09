"""
A Module to interact with Logic.

Defines LogicUI which you can use to interact with an
open instance of Logic.
"""
import time
import atomacos as ato
import keyboard as kb  # use for all keystrokes instead of atomacos because Dvorak
import subprocess

class LogicUI():
    """Interacts with Logic."""

    def __init__(self):
        """Creates a reference to atomacos' NativeUI whatever."""
        self.UI = ato.getAppRefByBundleId("com.apple.logic10")
        self.UI.activate()
        time.sleep(.5)  # necessary for fullscreen workflow (scroll-y animation switching screens)

    def __getWindowReference(self, window_title, timeout_s):
        windows = []
        attempts = 0
        while len(windows) == 0:
            if attempts * 0.1 > timeout_s:
                raise(Exception("Something went wrong getting window: " + window_title))
            time.sleep(0.1)
            windows = [
                window
                for window in self.UI.windows()
                if "AXTitle" in window.getAttributes() and window.AXTitle == window_title
            ]
            attempts += 1
        return windows[0]

    def toggleMixerOnOff(self):
        """
        Toggling the mixer closes any of the mixer, piano roll editor, etc.
        which ensures (well makes more likely anyway) it's focused on the
        track area.
        """
        self.UI.activate()
        old_num_children = len(self.UI.AXMainWindow.AXChildren)
        kb.send('x')
        mixer_closed = len(self.UI.AXMainWindow.AXChildren) < old_num_children
        if mixer_closed:
            print("Mixer already open, closed it.")
        else:
            print("Toggling mixer open/closed")
            kb.send('x')

    def goToLeftLocator(self):
        """Move the playhead to the left locator."""
        print("Moving playhead to left locator...")
        self.UI.activate()
        self.UI.menuItem("Navigate", "Go To", "Left Locator").Press()

    def importMidi(self, midiFile):
        print(midiFile)
        self.UI.activate()
        print("Opening up midi selection window...")
        self.UI.menuItem("File", "Import", "MIDI File…").Press()
        import_window = self.__getWindowReference("Import", 3)
        print(type(import_window))

        print("Navigating to folder...")
        kb.send('command+shift+g')
        time.sleep(1)
        subprocess.run("pbcopy", text=True, input=midiFile)
        kb.send('command+v')  # copy/paste is way faster than kb.write()
        time.sleep(1)
        kb.send('enter')

        print("Pressing import...")
        time.sleep(1)
        import_window.buttons("Import")[0].Press()

        print("Midi file imported")

    def selectLastTracks(self, select_num, total_num):
        """Select the last select_num tracks, assuming there are < total_num tracks."""
        self.UI.activate()
        # This is gross but prevents edge case where this doesn't work because
        # all (or most) tracks are already selected
        self.UI.menuItem("Track", "New Audio Track").Press()
        kb.send('delete')

        print("Moving selection down by", total_num)
        for i in range(total_num):
            kb.send('down')
        for i in range(select_num - 1):
            kb.send('shift+up')

    def move_last_tracks_to_prev_tracks(self, num_tracks):
        self.UI.activate()
        self.selectLastTracks(num_tracks, num_tracks * 2 + 10)
        kb.send('command+x')
        kb.send('delete')
        for i in range(num_tracks - 1):
            kb.send('shift+up')
        for i in range(num_tracks - 1):
            kb.send('up')
        kb.send('delete')  # Assumes they're populated
        kb.send('command+v')
        paste_window = self.__getWindowReference("Paste on Multiple Tracks", 3)
        paste_window.radioButtons("Use the selected and following tracks")[0].Press()
        paste_window.buttons("OK")[0].Press()

    def delete_last_tracks_regions(self, num_tracks):
        self.UI.activate()
        self.selectLastTracks(num_tracks, num_tracks + 10)
        kb.send('delete')
