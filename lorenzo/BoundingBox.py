class BoundingBox:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h

    def coords(self):
        return (self.x, self.y)

    def ends(self):
        return (self.x + self.w, self.y + self.h)
