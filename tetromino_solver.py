from tetromino import *

class Board:
    def __init__(self, width, height, content=None, occupancy=None):
        self.width = width
        self.height = height
        self.content = [] if content is None else content.copy()
        self.occupancy = {(x, y): 0 for x in range(width) for y in range(height)} if occupancy is None else occupancy.copy()

    def write(self, t, x=0, y=0):
        b = Board(self.width, self.height, self.content, self.occupancy)
        for p in t.points:
            p1 = (int(p[0] + x), int(p[1] + y))
            if p1[0] < 0 or p1[0] >= b.width or p1[1] < 0 or p1[1] >= b.height:
                raise IndexError('out of bounds')
            if b.occupancy[p1]:
                raise ValueError('already occupied')
            b.occupancy[p1] = 1
        b.content.append(t + (x, y))
        return b

    def conn_comp(self, visited, x=0, y=0, v=0):
        if (x, y) not in self.occupancy or (x, y) in visited or self.occupancy[x, y] != v:
            return
        visited.add((x, y))
        self.conn_comp(visited, x - 1, y, v)
        self.conn_comp(visited, x + 1, y, v)
        self.conn_comp(visited, x, y - 1, v)
        self.conn_comp(visited, x, y + 1, v)

    def pick(self, v=0):
        for p, w in self.occupancy.items():
            if w == v:
                return p

    def dump(self):
        data = {}
        for c, t in zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789=+"§±@#$%&*', self.content):
            for p in t.points:
                data[p] = c
        for y in reversed(range(self.height)):
            print(''.join(data.get((x, y), '.') for x in range(self.width)))

def solve(b, population):
    if sum(population.values()) == 0:
        print('solution:')
        b.dump()
        print('-' * 30)
        yield b
    else:
        # ensure that there is only one connected component of empty cells:
        ep = b.pick(0)
        if ep:
            ex, ey = ep
            cc = set()
            b.conn_comp(cc, ex, ey, 0)
            if len(cc) != sum(map(lambda x: x == 0, b.occupancy.values())):
                return

        b.dump()
        print('-' * 30)

        for p0, count in population.items():
            if count == 0: continue
            population1 = population.copy()
            population1[p0] -= 1
            pv = sorted(set(p0.r(rj).m(fx, fy) for rj in range(4) for fx in (1, -1) for fy in (1, -1)))
            for x in range(b.width):
                for y in range(b.height):
                    for p1 in pv:
                        p = p1 + (x, y)
                        tb = p.border()
                        if b.content and not any(b.occupancy.get(bp, 0) for bp in tb.points):
                            continue
                        try:
                            yield from solve(b.write(p), population1)
                        except (IndexError, ValueError):
                            pass

if __name__ == '__main__':
    b = Board(10, 8)
    population = {Tetromino.L: 5, Tetromino.I: 5, Tetromino.T: 5, Tetromino.S: 5}
    #b = Board(5, 4)
    #population = {Tetromino.L: 1, Tetromino.I: 1, Tetromino.T: 2, Tetromino.S: 1}

    for s in solve(b, population):
        print('found solution:')
        s.dump()
        break

