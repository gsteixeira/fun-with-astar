

from astar.search import AStar

if __name__ == "__main__":
    # Make a map (any size!)
    grid = [
        [0,0,0],
        [1,1,0],
        [0,0,0],
    ]
    # set start and end goals as (x, y) (vertical, horizontal)
    start = (0, 0)
    goal = (2, 0)

    # search
    path = AStar(grid).search(start, goal)
        
    # path should be:
    assert path == [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0)]

    print(path)
