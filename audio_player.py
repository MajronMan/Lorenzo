import pygame
import pygame.midi


class Player:
    def init(self):
        self.active_note = None
        pygame.midi.init()
        self.player = pygame.midi.Output(1)
        self.player.set_instrument(0, 0)

    def play(self, pitch, volume):
        if self.active_note[0] != pitch:
            self.player.note_off(self.active_note[0], self.active_note[1])
            self.player.note_on(pitch, volume)
            self.active_note = (pitch, volume)

    def quit(self):
        del self.player
        pygame.midi.quit()


player = Player()


def play_audio(pitch, volume):
    player.play(pitch, volume)


def init_audio():
    player.init()


def quit_audio():
    player.quit()
