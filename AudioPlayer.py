import random

import pygame
import pygame.midi
import time


class AudioPlayer:
    BPM = 80

    def __init__(self):
        self.active_note = None

        pygame.midi.init()
        self.drum_pitch = 30
        self.drum_vol = 50
        self.drum_channel = 2
        self.player = pygame.midi.Output(1)
        self.player.set_instrument(0)
        self.player.set_instrument(47, self.drum_channel)


        self.active_chord = None

    def play(self, notes):
        for (pitch, volume, duration) in notes:
            self.play_note(pitch, volume)
            time.sleep(duration * 60 / AudioPlayer.BPM)

    def play_note(self, pitch, volume):
        if self.active_note is None:
            self.active_note = (pitch, volume)
            self.player.note_on(pitch, volume)
        else:  # self.active_note[0] != pitch:
            self.player.note_off(self.active_note[0], self.active_note[1])
            self.player.note_on(pitch, volume)
            self.active_note = (pitch, volume)

    def close(self):
        self.player.close()
        pygame.midi.quit()

    def play_chord(self, pitches, volume):
        if self.active_chord is None:
            self.active_chord = (pitches, volume)
            self.active_note = (pitches[0], volume)
            for pitch in pitches:
                self.player.note_on(pitch, volume)
        else:
            active_pitches, vol = self.active_chord
            for pitch in active_pitches:
                self.player.note_off(pitch, vol)
            for pitch in pitches:
                self.player.note_on(pitch, vol)
            self.active_chord = (pitches, volume)



    def play_multiple_chords(self, notes):
        for (pitches, volume, duration) in notes:
            self.play_chord(pitches, volume)
            # self.player.note_on(self.drum_pitch, self.drum_vol, self.drum_channel)
            time.sleep(duration * 60 / AudioPlayer.BPM)
            # self.player.note_off(self.drum_pitch, self.drum_vol, self.drum_channel)
