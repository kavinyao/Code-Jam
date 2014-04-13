"""
Precompute shortest path to any point with 0<=|x|,|y|<=100
"""

import Queue
import random
import itertools

class Move(object):
    def __init__(self, direction, pos, next_units, parent=None):
        self.direction = direction
        self.pos = pos
        self.next_units = next_units
        self.parent = parent

    def __str__(self):
        return 'Move %s to %s' % (self.direction, self.pos)

def generate_path(move):
    directions = []
    while move:
        directions.append(move.direction)
        move = move.parent
    return ''.join(reversed(directions))

def remove_positions(rep_pos, pairs, solved_pairs):
    Ts = ((1, 1), (1, -1), (-1, 1), (-1, -1))
    for T in Ts:
        pos = (rep_pos[0] * T[0], rep_pos[1] * T[1])
        if pos in pairs:
            pairs.remove(pos)
            solved_pairs.add(pos)

def precompute(max_abs_x, max_abs_y):
    pairs = set(itertools.product(xrange(-max_abs_x, max_abs_x+1), xrange(-max_abs_y, max_abs_y+1))) 
    solved_pairs = set()
    solutions = {}
    queue = Queue.Queue()
    initial_move = Move('', (0, 0), 1)
    queue.put(initial_move)

    direction_offsets = [
        ('E', (1, 0)),
        ('N', (0, 1)),
        ('W', (-1, 0)),
        ('S', (0, -1))
    ]

    while len(pairs) > 4:
        current_move = queue.get()
        current_pos = current_move.pos
        current_units = current_move.next_units

        if current_pos in solved_pairs or (abs(current_pos[0]) > max_abs_x and abs(current_pos[1]) > max_abs_y):
            continue

        if current_pos in pairs:
            # solve all four positions
            rep_pos = (abs(current_pos[0]), abs(current_pos[1]))
            solutions[rep_pos] = (current_pos, generate_path(current_move))
            print 'solved', rep_pos, 'with', generate_path(current_move), 'left', len(pairs)

            remove_positions(rep_pos, pairs, solved_pairs)

        # generate more moves
        random.shuffle(direction_offsets)# let's go crazy
        for direction, offset in direction_offsets:
            new_pos = (current_pos[0]+offset[0]*current_units, current_pos[1]+offset[1]*current_units) 
            next_move = Move(direction, new_pos, current_units+1, current_move)
            queue.put(next_move)

    return solutions

if __name__ == '__main__':
    import sys
    import cPickle as pickle
    x, y = int(sys.argv[1]), int(sys.argv[2])
    solutions = precompute(x, y)
    pickle.dump(solutions, open('solution_%dx%d' % (x, y), 'wb'))
