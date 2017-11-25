import pygame
import pygame.midi


class Player:
    def init(self):
        self.active_note = None
        pygame.midi.init()
<<<<<<< Updated upstream
        self.player = pygame.midi.Output(1)
        self.player.set_instrument(17)
=======
        self.player = pygame.midi.Output(0)
        self.player.set_instrument(0, 0)
>>>>>>> Stashed changes

    def play(self, pitch, volume):
        if self.active_note is None:
            self.active_note = (pitch, volume)
            self.player.note_on(pitch, volume)
        elif self.active_note[0] != pitch:
            self.player.note_off(self.active_note[0], self.active_note[1])
            self.player.note_on(pitch, volume)
            self.active_note = (pitch, volume)

    def quit(self):
        del self.player
        pygame.midi.quit()


player = Player()


def play(pitch, volume):
    player.play(pitch, volume)


def init():
    player.init()


def quit():
    player.quit()
