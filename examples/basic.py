"""Basic version of A_Star
Very basic and procedural version of A*

This is for educational purposes only so very simplistic.

"""
from time import sleep

class Tile:
    """A tile represents a walkable square on a map.
    """
    distance = 0
    came_from = None
    weight = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        assert (self.x is not None and self.y is not None)

    def update_origin(self, came_from):
        """Update which tile this one came from."""
        self.came_from = came_from
        self.distance = came_from.distance + self.weight
    
    def __eq__(self, other):
        """A tile is the same if they have the same position"""
        return (other and self.x == other.x and self.y == other.y)

    def __hash__(self):
        """We need this so we can use a set()"""
        return hash(str(self))

    @property
    def pos(self):
        return (self.x, self.y)

    def __str__(self):
        return str(self.pos)

    def __repr__(self):
        return str(self)

def a_star(world, start_pos, target_pos):
    """A_Star (A*) path search algorithm"""
    print(start_pos)
    start = Tile(*start_pos)
    open_tiles = set([start])
    closed_tiles = set()

    # while we still have tiles to search
    while len(open_tiles) > 0:
        current = get_closest(open_tiles)

        if current.pos == target_pos:
            return rebuild_path(current)

        # do de search
        for candidate in get_neighbors(world, current):
            # if this is a new tile, add it
            if (candidate not in open_tiles
                and candidate not in closed_tiles):
                candidate.update_origin(current)
                open_tiles.add(candidate)

            # if this candidate has gone a farthest distance before,
            #   then we just found a new shortest way to it
            elif candidate.distance > current.distance + 1: # weight
                candidate.update_origin(current)
                # if it was close, reopen
                if candidate in closed_tiles:
                    closed_tiles.remove(candidate)
                    open_tiles.add(candidate)

        # remove current from open_tiles, as we had tested it
        open_tiles.remove(current)
        closed_tiles.add(current)
    print("Path blocked!!")


def get_neighbors(grid, tile):
    """return a list of available tiles around a given tile"""
    min_x = max(0, tile.x - 1)
    max_x = min(len(grid) - 1, tile.x + 1)
    min_y = max(0, tile.y - 1)
    max_y = min(len(grid[tile.x]) - 1, tile.y + 1)

    available_tiles = [
        (min_x, tile.y),
        (max_x, tile.y),
        (tile.x, min_y),
        (tile.x, max_y),
    ]
    neighbors = []
    for x, y in available_tiles:
        if (x, y) == tile.pos:
            continue

        if grid[x][y] == 0:
            neighbors.append(Tile(x, y))

    return neighbors


def get_closest(open_tiles):
    """Given a list of tiles, return the one that has walked shortest distanc"""
    closer = None
    for tile in open_tiles:
        if closer is None or closer.distance > tile.distance + 1:
            closer = tile
    return closer


def rebuild_path(current):
    """Rebuild the path from each tile"""
    path = []
    while current is not None:
        path.append(current)
        current = current.came_from
    path.reverse()
    return path

# Enf of A*.

# Those functions are for animation only
def walk_through(world, path):
    """Plays the animation of the character walking through the maze"""
    if not path:
        return
    for tile in path:
        x, y = tile.pos
        world[x][y] = 2
        print_map(world)
        sleep(0.1)
        world[x][y] = 4
    
def print_map(grid):
    """Print the map"""
    sprints = {
        0: " ",
        1: "#",
        2: "*",
        4: ".",
        }
    print("------------------")
    for line in grid:
        row = ' '.join([sprints[x] for x in line])
        print(row)



if __name__ == "__main__":

    world = [
        [0,1,0,1,0,0,0],
        [0,1,0,0,0,1,0],
        [0,0,0,0,1,0,0],
        [1,1,1,1,1,0,1],
        [0,0,0,0,1,0,0],
        [0,1,0,0,0,0,0],
        ]

    start = (0,0)
    goal = (5,0)

    path = a_star(world, start, goal)

    print(path)
    walk_through(world, path)
