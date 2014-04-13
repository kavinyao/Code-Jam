# -*- coding:utf-8 -*-
import os
import sys
from collections import defaultdict
import itertools


class State(object):
    _id = 1

    """A state of chest opening process."""
    def __init__(self, key_states, chest_states, parent_state):
        self.id = State._id
        State._id += 1

        self.key_states = key_states
        self.chest_states = chest_states
        self.parent_state = parent_state

        keys_in_hand = set((k for k, n in key_states.iteritems() if n > 0))
        # reverse for the convenience of popping
        self.choices_left = sorted(itertools.ifilter(lambda c: not chest_states[c], itertools.chain(*[State.key_chest_mapping[k] for k in keys_in_hand])), reverse=True)

    def is_initial(self):
        return self.parent_state == None

    def all_open(self):
        return all(self.chest_states[1:])

    def no_choices_left(self):
        return len(self.choices_left) == 0

    def open_sequence(self):
        chests = []
        state = self.parent_state
        while state != None:
            chests.append(state.current_choice)
            state = state.parent_state
        return ' '.join(map(str, reversed(chests)))

    def choose(self):
        if self.no_choices_left():
            return self.parent_state

        # use the smallest one to ensure lexicographical order
        chest_to_open = self.choices_left.pop()
        self.current_choice = chest_to_open
        print 'Opening chest', chest_to_open

        new_chest_states = list(self.chest_states)
        new_chest_states[chest_to_open] = True
        new_key_states = self._update_key_states(chest_to_open)

        return State(new_key_states, new_chest_states, self)

    def _update_key_states(self, opened_chest):
        new_key_states = {}
        for k in xrange(1, State.K+1):
            n = self.key_states.get(k, 0)
            if opened_chest in State.key_chest_mapping[k]:
                # used, decrement left number
                n -= 1
            n += State.chest_key_mapping[opened_chest].count(k)
            new_key_states[k] = n
        return new_key_states

    def __str__(self):
        return "State<%d>: %s, C:%s, K:%s" % (self.id, self.choices_left, self.chest_states, self.key_states)


def solve(N, key_chest_mapping, chest_key_mapping, initial_keys):
    # some prelimiary check
    all_keys = list(itertools.chain(initial_keys, *chest_key_mapping.values()))
    if len(all_keys) < N:
        return 'IMPOSSIBLE'

    for key, chests in key_chest_mapping.iteritems():
        if all_keys.count(key) < len(chests):
            return 'IMPOSSIBLE'

    print 'IK', initial_keys
    print 'KCM', key_chest_mapping
    print 'CKM', chest_key_mapping

    # reset ID
    State._id = 1
    # the mappings are readonly
    State.K = len(key_chest_mapping.keys())
    State.key_chest_mapping = key_chest_mapping
    State.chest_key_mapping = chest_key_mapping

    # key_states indicates the number of each key in hand
    key_states = {k: len(list(g)) for k, g in itertools.groupby(sorted(initial_keys))}
    # chest_states indicates whether a chest is opened
    # the initial is all False
    chest_states = [False for i in range(N+1)]

    # create initial state
    current_state = State(key_states, chest_states, None)
    while True:
        print current_state

        if current_state.all_open():
            break

        if current_state.is_initial() and current_state.no_choices_left():
            break

        # do transitions
        next_state = current_state.choose()
        current_state = next_state

    if current_state.all_open():
        return current_state.open_sequence()
    else:
        return 'IMPOSSIBLE'


if __name__ == '__main__':
    in_file = sys.argv[1]
    out_file = os.path.splitext(in_file)[0] + '.out'
    output = open(out_file, 'w')

    with open(in_file) as test:
        rounds = int(test.next())
        print rounds, 'rounds'

        for i in xrange(rounds):
            print 'round', i+1
            K, N = map(int, test.next().split())
            initial_keys = map(int, test.next().split())
            # key_chest_mapping indicates which chests can be opened by given key
            key_chest_mapping = defaultdict(set)
            # chest_key_mapping indicates what keys are stored in given chest
            chest_key_mapping = {}

            for j in xrange(N):
                config = map(int, test.next().split())
                key_chest_mapping[config[0]].add(j+1)
                chest_key_mapping[j+1] = config[2:]

            res = solve(N, key_chest_mapping, chest_key_mapping, initial_keys)
            print res
            output.write("Case #%d: %s\n" % (i+1, res))
            print

    output.close()
