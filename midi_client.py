import time
import rtmidi
from notes import Notes
from chord_types import ChordTypes

class MidiClient:

    midiout = None
    root_note_a_midi = 45
    # Change this after you've run the script once to determined the port loopMIDI is running on.
    midi_port = 2

    def __init__(self):
        self.midiout = rtmidi.MidiOut()
        available_ports = self.midiout.get_ports()

        # here we're printing the ports to check that we see the one that loopMidi created. 
        # In the list we should see a port called "loopMIDI port".
        print(available_ports)

        # Attempt to open the port
        if available_ports:
            self.midiout.open_port(midi_port)
        else:
            self.midiout.open_virtual_port("My virtual output")

    def __del__(self):
        self.all_notes_off()

    def test(self):
        self.play_chord(60, 0.75)
        self.play_chord(65, 0.5)
        self.play_chord(65, 0.25, True)
        self.play_chord(67, 0.5)
        self.play_chord(60, 1)

    def on_chord_change(self, root_note: Notes, chord_type: ChordTypes, old_root_note: Notes, old_chord_type: ChordTypes):
        self.all_notes_off()
        if (root_note and chord_type):
            notes = self.get_notes_for_chord(root_note, chord_type)
            for note_midi in notes:
                self.note_on(note_midi)
        print("Changing chord from {} {} to {} {}.".format(old_root_note, old_chord_type, root_note, chord_type))

    def get_notes_for_chord(self, root_note: Notes, chord_type: ChordTypes):
        notes = []
        root_note_midi = self.root_note_a_midi + root_note.value
        notes.append(root_note_midi)
        if (chord_type == ChordTypes.major):
            pass
        elif (chord_type == ChordTypes.minor):
            notes.append(root_note_midi + 3)
        elif (chord_type == ChordTypes.diminished):
            notes.append(root_note_midi + 3)
            notes.append(root_note_midi + 6)
        elif (chord_type == ChordTypes.major_seventh):
            notes.append(root_note_midi + 4)
            notes.append(root_note_midi + 7)
            notes.append(root_note_midi + 11)
        elif (chord_type == ChordTypes.minor_seventh):
            notes.append(root_note_midi + 3)
            notes.append(root_note_midi + 7)
            notes.append(root_note_midi + 10)
        elif (chord_type == ChordTypes.dominant_seventh):
            notes.append(root_note_midi + 4)
            notes.append(root_note_midi + 7)
            notes.append(root_note_midi + 10)
        elif (chord_type == ChordTypes.suspended):
            notes.append(root_note_midi + 5)
            notes.append(root_note_midi + 7)
        elif (chord_type == ChordTypes.augmented):
            notes.append(root_note_midi + 4)
            notes.append(root_note_midi + 8)
        return notes

    def all_notes_off(self):
        all_notes_off = [0xB0, 123, 0]
        self.midiout.send_message(all_notes_off)

    def note_on(self, note):
        note_on = [0x90, note, 100]
        self.midiout.send_message(note_on)

    def note_off(self, note):
        note_off = [0x80, note, 0]
        self.midiout.send_message(note_off)

    def do_stroke(self, upstroke=False):
        downstroke = 24 if upstroke == False else 26
        note_on = [0x90, downstroke, 100]
        note_off = [0x80, downstroke, 0]
        self.midiout.send_message(note_on)
        self.midiout.send_message(note_off)

    def play_chord(self, note, duration, upstroke=False):
        self.note_on(note)
        self.do_stroke(upstroke=upstroke)
        time.sleep(duration)
        self.all_notes_off()


if __name__ == "__main__":
    midi_client = MidiClient()

    midi_client.test()

    del midi_client

