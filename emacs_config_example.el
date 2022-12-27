(setq lilypond-default-num-of-staves 4)
(defun lilypond-send-midi-to-logic (n)
    (interactive
     (list (read-number
            (format "Number of instruments: ")
            lilypond-default-num-of-staves
            ))
     LilyPond-mode)
    (setq lilypond-default-num-of-staves n)
    (shell-command
     (concat
      "/Users/josh/Documents/csstuff/lilyPond/import_midi_to_logic/import_midi_to_logic.py "
      (if (not (equal current-prefix-arg nil)) "--first ")
      (number-to-string (+ n 1)) " " ; Add 1 because LilyPond adds one more track than there are staves
      "'" buffer-file-name "'")
    (get-buffer-create "*Standard output*")))
(map! :desc "Send midi from current lilypond buffer to active Logic session. Prefix C-u if it's the first time for this Logic file."
      :mode LilyPond-mode
      "C-c C-a" 'lilypond-send-midi-to-logic)
