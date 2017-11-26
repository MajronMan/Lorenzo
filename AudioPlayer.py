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
        self.player.set_instrument(1)

    def play(self, notes):
        for (pitch, volume, duration) in notes:
            self.play_note(pitch, volume)
            time.sleep(duration * 60 / AudioPlayer.BPM)

    def play_note(self, pitch, volume):
        if self.active_note is None:
            self.active_note = (pitch, volume)
            self.player.note_on(pitch, volume)
            self.player.note_on(pitch + 5, volume)
        else:  # self.active_note[0] != pitch:
            self.player.note_off(self.active_note[0], self.active_note[1])
            self.player.note_off(self.active_note[0] + 3, self.active_note[1])
            self.player.note_on(pitch, volume)
            self.player.note_on(pitch + 5, volume)
            self.active_note = (pitch, volume)

    def close(self):
        self.player.close()
        pygame.midi.quit()
