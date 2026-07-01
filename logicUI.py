"""
A Module to interact with Logic.

Defines LogicUI which you can use to interact with an
open instance of Logic.
"""
import time
import atomacos as ato
from pynput.keyboard import Key, Controller  # use for all keystrokes instead of atomacos because Dvorak
import subprocess


kb = Controller()

def hotkey(*args):
    for key in args:
        kb.press(key)
    for key in reversed(args):
        kb.release(key)


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
        hotkey('x')
        mixer_closed = len(self.UI.AXMainWindow.AXChildren) < old_num_children
        if mixer_closed:
            print("Mixer already open, closed it.")
        else:
            print("Toggling mixer open/closed")
            hotkey('x')

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
        time.sleep(.2)
        import_window = self.__getWindowReference("Import", 3)

        print("Navigating to folder...")
        time.sleep(0.3)
        hotkey(Key.cmd, Key.shift, 'g')
        time.sleep(0.5)
        subprocess.run("pbcopy", text=True, input=midiFile)
        hotkey(Key.cmd, 'v')
        time.sleep(.1)
        hotkey(Key.enter)

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
        hotkey(Key.delete)

        print("Moving selection down by", total_num)
        for _ in range(total_num):
            hotkey(Key.down)
        for _ in range(select_num - 1):
            hotkey(Key.shift, Key.up)

    def move_last_tracks_to_prev_tracks(self, num_tracks):
        self.UI.activate()
        self.selectLastTracks(num_tracks, num_tracks * 2 + 10)
        hotkey(Key.cmd, 'x')
        hotkey(Key.delete)
        for _ in range(num_tracks - 1):
            hotkey(Key.shift, Key.up)
        for _ in range(num_tracks - 1):
            hotkey(Key.up)
        hotkey(Key.delete)  # Assumes they're populated
        hotkey(Key.cmd, 'v')
        paste_window = self.__getWindowReference("Paste on Multiple Tracks", 3)
        paste_window.radioButtons("Use the selected and following tracks")[0].Press()
        paste_window.buttons("OK")[0].Press()

    def delete_last_tracks_regions(self, num_tracks):
        self.UI.activate()
        self.selectLastTracks(num_tracks, num_tracks + 10)
        hotkey(Key.delete)
