import random

from lorenzo.auralization import random_with_distribution, bounded_add, get_scale_octaves


class Auralizer:
    prev_base = None

    def __init__(self, current_scale, base_sound):
        self.scale = get_scale_octaves(current_scale, base_sound)
        self.prev_base_ind = None
        minimum = self.scale[0]
        maximum = self.scale[-1]
        self.prob = lambda x: x / (minimum - maximum) - maximum / (minimum - maximum)

    def get_next_base(self, dominant):
        if self.prev_base_ind is None:
            self.prev_base_ind = 8

        last_pitch = self.scale[self.prev_base_ind]
        move_right = self.prob(last_pitch)
        r = (dominant if random.random() < move_right else -dominant)
        new_base_ind = bounded_add(self.prev_base_ind, r, 0, len(self.scale) - 1)
        new_base = self.scale[new_base_ind]

        self.prev_base_ind = new_base_ind
        return (new_base_ind, new_base)

    def build_chord(self, dominant):
        new_base_ind, new_base = self.get_next_base(dominant)
        pitches = [new_base]
        for i in range(1, 4):
            if random.random() < (0.2) ** i:
                pitches.append(self.scale[bounded_add(new_base_ind, 2 * i, 0, len(self.scale) - 1)])
        return pitches
