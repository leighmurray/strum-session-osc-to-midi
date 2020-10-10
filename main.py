from midi_client import MidiClient
from osc_server import OSCServer, Pitch
from state_machine import StateMachine
from notes import Notes
from chord_types import ChordTypes
import time

def run():
    state_machine = StateMachine()
    midi_client = MidiClient()
    osc_server = OSCServer("192.168.137.1")

    state_machine.on_change_chord.append(midi_client.on_chord_change)
    state_machine.on_stroke.append(midi_client.do_stroke)

    # input handling
    osc_server.on_button_press.append(state_machine.input_on_button_press)
    osc_server.on_pitch_change.append(state_machine.input_on_pitch_change)
    osc_server.on_acceleration.append(state_machine.input_on_acceleration)

    osc_server.serve()

    del midi_client


def test_chords():
    state_machine = StateMachine()

    midi_client = MidiClient()
    
    state_machine.on_change_chord.append(midi_client.on_chord_change)
    sleep_time = 1
    state_machine.set_current_chord(Notes.c, ChordTypes.major)
    midi_client.do_stroke()
    time.sleep(sleep_time)
    state_machine.set_current_chord(Notes.c, ChordTypes.minor)
    midi_client.do_stroke()
    time.sleep(sleep_time)
    state_machine.set_current_chord(Notes.c, ChordTypes.diminished)
    midi_client.do_stroke()
    time.sleep(sleep_time)
    state_machine.set_current_chord(Notes.c, ChordTypes.major_seventh)
    midi_client.do_stroke()
    time.sleep(sleep_time)
    state_machine.set_current_chord(Notes.c, ChordTypes.minor_seventh)
    midi_client.do_stroke()
    time.sleep(sleep_time)
    state_machine.set_current_chord(Notes.c, ChordTypes.dominant_seventh)
    midi_client.do_stroke()
    time.sleep(sleep_time)
    state_machine.set_current_chord(Notes.c, ChordTypes.suspended)
    midi_client.do_stroke()
    time.sleep(sleep_time)
    state_machine.set_current_chord(Notes.c, ChordTypes.augmented)
    midi_client.do_stroke()
    time.sleep(sleep_time)
    del midi_client


if __name__ == "__main__":
    run()
