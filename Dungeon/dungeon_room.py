DIRECTIONS = {"N", "S", "E", "W"}
OPPOSITE = {"N": "S", "S": "N", "E": "W", "W": "E"}


class DungeonRoom:
    def __init__(self, x, y, is_start, is_exit):
        self.x = x
        self.y = y
        self.neighbors = {}
        self.enemies = []
        self.visited = False
        self.visible = False
        self.is_current = False
        self.is_exit = is_exit
        self.is_start = is_start

    def connect(self, neighbor, direction):
        if direction not in DIRECTIONS:
            print(f"Nesipravni susjed od {self.x},{self.y}")
            return
        self.neighbors[direction] = neighbor
        neighbor.neighbors[OPPOSITE[direction]] = self

    def get_unvisited_neighbors(self):
        return [room for room in self.neighbors.values() if not room.visited]

    def reveal_neighbors(self):
        for neighbor in self.neighbors.values():
            neighbor.visible = True

    def get_icon(self):
        if not self.visible:
            return "undiscovered.png"
        directions_order = ["N", "E", "S", "W"]
        connections = ""
        for direction in directions_order:
            if direction in self.neighbors:
                connections += direction
        if not connections:
            return "dead_end.png"
        if self.is_current:
            return f"{connections}_current.png"
        return f"{connections}.png"
