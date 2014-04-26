NOTES = ["A", "A^", "B", "C", "C^", "D", "D^", "E", "F", "F^", "G", "G^"]


class Note:
    def __init__(self, frequency, duration):
        self.frequency = frequency
        self.duration = duration

    def play(self, robot):
        robot.power.beep(self.frequency, self.duration)
        sleep(self.duration)


class Tune:
    def __init__(self):
        self.title = "Untitled"
        self.unit = 0.25
        self.tempo = 120
        self.data = []

    def play(self, robot):
        for note in self.data:
            note.play(robot)


class ABC:
    def __init__(self, path):
        self.tunes = {}
        with open(path) as file:
            reference = 0
            repeat = False
            buffer = []
            for line in file:
                if reference:
                    tune = self.tunes[reference]
                    if line[0] == "T":
                        tune.title = line[2:].strip()
                        continue
                    elif line[0] == "L":
                        length = tuple(map(float, line[2:].strip().split("/")))
                        tune.unit = length[0] / length[1]
                        continue
                    elif line[0] == "Q":
                        bpm = line[2:].strip().split("=")[-1]
                        tune.tempo = int(bpm)
                        continue
                    elif line[0] in "ABCDFGHIKLMmNOPQRrSsTUVWwXZ":
                        # This metadata is not important.
                        continue

                    # Begin reading tune.
                    i = 0
                    while i < len(line):
                        # Begin repeated section.
                        if line[i:i+2] == "|:":
                            repeat = True
                            i += 2
                            continue

                        # End repeated section.
                        if line[i:i+2] == ":|":
                            repeat = False
                            tune.data.extend(buffer)
                            buffer = []
                            i += 2
                            continue

                        # Read note data.
                        if line[i].upper() in NOTES:
                            # Check note letter.
                            note = line[i].upper()
                            i += 1
                            if line[i] in ["^", "_"]:
                                note += line[i]
                            else: i -= 1

                            # Check octave.
                            octave = -1 if line[i] in ascii_uppercase else 0
                            i += 1
                            while line[i] in ["'", ","]:
                                octave += 1 if line[i] == "'" else -1
                                i += 1
                            else: i -= 1

                            # Check note length.
                            i += 1
                            try:
                                length = int(line[i])
                            except:
                                length = 1
                                i -= 1

                            # Add note to tune.
                            exponent = octave + NOTES.index(note) / 12
                            frequency = 440 * 2**exponent
                            duration = tune.unit * tune.tempo/60 * length
                            tune.data.append(Note(frequency, duration))
                            if repeat:
                                buffer.append(Note(frequency, duration))
                        i += 1
                elif line[0] == "X":
                    reference = int("0" + line[2:].strip())
                    self.tunes[reference] = Tune()

    def play(self, robot, reference):
        self.tunes[reference].play(robot)
