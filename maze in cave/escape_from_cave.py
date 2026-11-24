import random


class Item:
    def __init__(self, n, k, w, v):
        self.n = n
        self.k = k
        self.w = w
        self.v = v

    def __repr__(self):
        return f"{self.n} (weight: {self.w}, value: {self.v})"

    @staticmethod
    def start():
        return [Item("food", "food", 0.5, 5) for _ in range(2)] + [Item("torch", "torch", 1.0, 2)]

    @staticmethod
    def loot():
        p = [
            Item("food", "food", 0.5, 5),
            Item("torch", "torch", 1.0, 2),
            Item("rope", "rope", 1.0, 3),
            Item("coin", "gold", 0.1, 50),
            Item("rock", "junk", 4.0, 0),
        ]
        return [random.choice(p) for _ in range(random.randint(1, 2))]


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.mx = 25
        self.e = 25
        self.cap = 12
        self.cr = 0
        self.inv = Item.start()

    def weight(self):
        return sum(i.w for i in self.inv)

    def score(self):
        return sum(i.v for i in self.inv) + 100 * self.cr

    def add(self, item):
        self.inv.append(item)

    def add_all(self, items):
        ok = []
        w = self.weight()
        for i in items:
            if w + i.w <= self.cap:
                ok.append(i)
                w += i.w
            else:
                print(f"too heavy, left: {i.n}")
        self.inv.extend(ok)

    def drop(self):
        if self.inv:
            return self.inv.pop()
        return None

    def find(self, n):
        names = [i.n for i in self.inv]
        if n in names:
            return names.index(n)
        return -1

    def remove(self, n):
        i = self.find(n)
        if i == -1:
            return None
        it = self.inv[i]
        self.inv.remove(it)
        return it

    def sort(self, by):
        if by == "val":
            self.inv.sort(key=lambda i: i.v)
        else:
            self.inv.sort(key=lambda i: i.w)

    def reverse(self):
        self.inv.reverse()

    def part(self, a, b):
        return self.inv[a:b]

    def top(self, k=3):
        c = self.inv.copy()
        c.sort(key=lambda i: i.v)
        c.reverse()
        return c[:k]

    def heal(self, n):
        self.e = min(self.mx, self.e + n)


class Room:
    def __init__(self, kind):
        self.kind = kind
        self.seen = False
        self.known = False
        self.loot = []


class Maze:
    def __init__(self, w=6, h=6):
        self.w = w
        self.h = h
        self.grid = {}
        self.generate()

    def generate(self):
        c = [(x, y) for x in range(self.w) for y in range(self.h)]
        for p in c:
            self.grid[p] = Room("empty")

        c.remove((0, 0))
        random.shuffle(c)

        self.grid[c.pop()] = Room("exit")

        for _ in range(3):
            self.grid[c.pop()] = Room("crystal")

        for _ in range(3):
            p = c.pop()
            self.grid[p] = Room("chest")
            self.grid[p].loot = Item.loot()

        for _ in range(2):
            self.grid[c.pop()] = Room("camp")

        for _ in range(3):
            self.grid[c.pop()] = Room("trap")

    def room(self, x, y):
        return self.grid.get((x, y))


class Game:
    D = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
    L = {"crystal": "C", "camp": "F", "chest": "B", "trap": "T", "exit": "E", "empty": "-"}

    def __init__(self):
        self.p = Player()
        self.m = Maze(6, 6)

    def help(self):
        print("\n--- commands ---")
        print(" w / a / s / d  - move (costs 1 energy)")
        print(" map            - show map")
        print(" i              - inventory")
        print(" use <name>     - use food or torch")
        print(" drop           - drop last item")
        print(" remove <name>  - drop item by name")
        print(" srt val / wt   - sort inventory by value / weight")
        print(" rev            - reverse inventory")
        print(" slice <a> <b>  - show part of inventory")
        print(" top            - 3 most valuable items")
        print(" q              - quit")

    def show_inv(self):
        p = self.p
        print("\n--- inventory ---")
        if not p.inv:
            print("empty")
        for n, i in enumerate(p.inv):
            print(f"{n + 1}. {i}")
        print(f"weight: {p.weight():.1f}/{p.cap} | crystals: {p.cr}/3")

    def show_map(self):
        for y in range(self.m.h):
            s = ""
            for x in range(self.m.w):
                r = self.m.room(x, y)
                if (x, y) == (self.p.x, self.p.y):
                    s += "P "
                elif r.seen:
                    s += "E " if r.kind == "exit" else ". "
                elif r.known:
                    s += self.L[r.kind] + " "
                else:
                    s += "? "
            print(s)
        print("P you, ? unknown, . visited, - empty, C crystal, F camp, B chest, T trap, E exit")

    def use(self, n):
        p = self.p
        i = p.find(n)
        if i == -1:
            print("error: no such item")
            return
        k = p.inv[i].k
        if k == "food":
            p.inv.pop(i)
            p.heal(8)
            print("energy +8")
        elif k == "torch":
            p.inv.pop(i)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    r = self.m.room(p.x + dx, p.y + dy)
                    if r:
                        r.known = True
            print("torch lit, nearby rooms revealed (see map)")
        else:
            print("error: cant use this item")

    def enter(self):
        p = self.p
        r = self.m.room(p.x, p.y)
        first = not r.seen
        r.seen = True

        if r.kind == "exit":
            if p.cr == 3:
                print(f"you escaped! score: {p.score()}")
                return True
            print(f"exit is locked: {p.cr}/3 crystals")
            return False

        if not first:
            return False

        if r.kind == "crystal":
            print("you found a crystal!")
            p.cr += 1
        elif r.kind == "camp":
            print("old camp. energy +10")
            p.heal(10)
        elif r.kind == "chest":
            print("you found a chest:")
            for i in r.loot:
                print(f" - {i.n}")
            p.add_all(r.loot)
            r.loot = []
        elif r.kind == "trap":
            i = p.find("rope")
            if i != -1:
                p.inv.pop(i)
                print("trap! rope used, you avoided it")
            else:
                print("trap! energy -6")
                p.e -= 6
        return False

    def run(self):
        p = self.p
        print("=" * 30)
        print("cave escape")
        print("find 3 crystals and reach the exit. h - help")
        print("=" * 30)

        while True:
            print(f"\n({p.x}, {p.y}) | energy: {p.e}/{p.mx} | crystals: {p.cr}/3")
            c = input("command: ").strip().lower()

            if c == 'q':
                print("you quit")
                break
            elif c == 'h':
                self.help()
            elif c in self.D:
                dx, dy = self.D[c]
                if self.m.room(p.x + dx, p.y + dy) is None:
                    print("error: wall")
                    continue
                p.x += dx
                p.y += dy
                p.e -= 1
                if self.enter():
                    break
                if p.e <= 0:
                    print("out of energy. game over")
                    break
            elif c == 'map':
                self.show_map()
            elif c == 'i':
                self.show_inv()
            elif c.startswith('use '):
                self.use(c[4:])
            elif c == 'drop':
                d = p.drop()
                print(f"dropped: {d.n}" if d else "error: inventory is empty")
            elif c.startswith('remove '):
                d = p.remove(c[7:])
                print(f"dropped: {d.n}" if d else "error: no such item")
            elif c in ('srt val', 'srt wt'):
                p.sort(c[4:])
                print("sorted")
            elif c == 'rev':
                p.reverse()
                print("reversed")
            elif c.startswith('slice '):
                try:
                    a, b = c.split()[1:3]
                    for i in p.part(int(a), int(b)):
                        print(f" - {i.n}")
                except ValueError:
                    print("error: usage: slice <a> <b>")
            elif c == 'top':
                for i in p.top():
                    print(f" - {i}")
            else:
                print("error: incorrect input, h - help")


if __name__ == "__main__":
    game = Game()
    game.run()
