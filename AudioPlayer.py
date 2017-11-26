import random

import pygame
import pygame.midi
import time


class AudioPlayer:
    BPM = 120
    METRUM = 4

    def __init__(self):
        self.active_note = None

        pygame.midi.init()
        self.player = pygame.midi.Output(1)
        self.player.set_instrument(81)

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
            for pitch in pitches:
                self.player.note_on(pitch, volume)
        else:
            active_pitches, vol = self.active_chord
            for pitch in active_pitches:
                self.player.note_off(pitch, vol)
            for pitch in pitches:
                self.player.note_on(pitch, vol)
            self.active_chord = (pitches, volume)

    def quit(self):
        del self.player
        pygame.midi.quit()


player = AudioPlayer()


def play(notes):
    for (scale, i0, volume, duration) in notes:
        pitches = [scale[i0]]
        r = random.Random()
        for i in range(1, 4):
            if random.random() < (0.2) ** i:
                pitches.append(scale[(i0 + i) % len(scale)])
        player.play_chord(pitches, volume)
        time.sleep(duration * 60 / BPM)

#
# def play_note(pitch, volume, duration):
#     player.play(pitch, volume)


def init():
    player.init()

