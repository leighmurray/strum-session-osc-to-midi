import event
from notes import Notes
from chord_types import ChordTypes
from pitch import Pitch

class StateMachine:
    current_root_note = None
    current_chord_type = None

    def __init__(self):
        self.on_change_chord = event.Event()
        self.on_stroke = event.Event()

    def get_current_chord(self):
        return self.current_chord

    def set_root_note(self, root_note: Notes):
        self.set_current_chord(root_note, self.current_chord_type)

    def set_chord_type(self, chord_type: ChordTypes):
        self.set_current_chord(self.current_root_note, chord_type)

    def input_on_pitch_change(self, pitch: Pitch):
        if pitch == Pitch.low:
            print("Setting Major")
            self.set_chord_type(ChordTypes.major)
        elif pitch == Pitch.middle:
            print("Setting Minor")
            self.set_chord_type(ChordTypes.minor)
        elif pitch == Pitch.high:
            print("Setting Dominant Seventh")
            self.set_chord_type(ChordTypes.dominant_seventh)

    def input_on_button_press(self, button_number: int):
        print("Button Number: {}".format(button_number))
        if button_number == 4:
            self.set_root_note(Notes.c)
        elif button_number == 8:
            self.set_root_note(Notes.d)
        elif button_number == 12:
            self.set_root_note(Notes.f)
        elif button_number == 16:
            self.set_root_note(Notes.g)

    def input_on_acceleration(self, axis, direction):
        print("Axis {} and acceleration {}".format(axis, direction))
        if direction == 1:
            print("Calling downstroke")
            self.on_stroke()
        else:
            print("Calling upstroke")
            self.on_stroke(True)

    def set_current_chord(self, root_note: Notes, chord_type: ChordTypes):
        old_root_note = self.current_root_note
        old_chord_type = self.current_chord_type

        self.current_root_note = root_note
        self.current_chord_type = chord_type
        self.on_change_chord(root_note, chord_type, old_root_note, old_chord_type)

def test_chord_change(root_note: Notes, chord_type: ChordTypes, old_root_note: Notes, old_chord_type: ChordTypes):
    print("Changing chord from {} {} to {} {}.".format(old_root_note, old_chord_type, root_note, chord_type))

def test():
    state_machine = StateMachine()
    state_machine.on_change_chord.append(test_chord_change)
    state_machine.set_current_chord(Notes.g_sharp, ChordTypes.major)
    state_machine.set_current_chord(Notes.c, ChordTypes.dominant_seventh)

if __name__ == "__main__":
    test()
