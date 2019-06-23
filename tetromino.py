class Tetromino:
    def __init__(self, initPoints=[]):
        iround = lambda x: int(round(x))
        self.points = set((iround(p[0]), iround(p[1])) for p in initPoints)

    def __add__(self, other):
        return Tetromino([(p[0] + other[0], p[1] + other[1]) for p in self.points])

    def __sub__(self, other):
        return self + tuple(-h for h in other)

    def __eq__(self, other):
        return self.points == other.points

    def __lt__(self, other):
        return sorted(self.points) < sorted(other.points)

    def __hash__(self):
        return hash((tuple(sorted(self.points))))

    def __str__(self):
        return str(self.points)

    def __repr__(self):
        return f'Tetromino({self.points})'

    def n(self):
        mx = min(p[0] for p in self.points)
        my = min(p[1] for p in self.points)
        return self - (mx, my)

    def r(self, a):
        from math import cos, sin, pi
        k = 0.5 * pi * a
        return Tetromino([(cos(k) * p[0] - sin(k) * p[1], sin(k) * p[0] + cos(k) * p[1]) for p in self.points]).n()

    def m(self, mx, my):
        return Tetromino([(p[0] * mx, p[1] * my) for p in self.points]).n()

    def expanded(self):
        return Tetromino([(p[0] + o[0], p[1] + o[1]) for o in ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)) for p in self.points])

    def border(self):
        return Tetromino(self.expanded().points - self.points)


Tetromino.L = Tetromino([(0, 0), (0, 1), (1, 0), (0, 2)])
Tetromino.I = Tetromino([(0, 0), (0, 1), (0, 2), (0, 3)])
Tetromino.T = Tetromino([(1, 0), (0, 1), (1, 1), (2, 1)])
Tetromino.S = Tetromino([(0, 0), (1, 0), (1, 1), (2, 1)])
