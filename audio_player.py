import pygame
import pygame.midi
import time

BPM = 120
METRUM = 4


class Player:
    def init(self):
        self.active_note = None
        pygame.midi.init()
        self.player = pygame.midi.Output(1)
        self.player.set_instrument(1)

    def play(self, pitch, volume):
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

    def quit(self):
        del self.player
        pygame.midi.quit()


player = Player()


def play(notes):
    for (pitch, volume, duration) in notes:
        player.play(pitch, volume)
        time.sleep(duration * 60 / BPM)


def play_note(pitch, volume, duration):
    player.play(pitch, volume)


def init():
    player.init()


def quit():
    player.quit()
