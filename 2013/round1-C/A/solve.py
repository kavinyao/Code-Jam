# -*- coding:utf-8 -*-
import os
import sys
import math
import string
import itertools

transtable = string.maketrans(
    'abcdefghijklmnopqrstuvwxyz',
    '01110111011111011111011111'
)

def solve(name, n):
    """Return n-value of name."""
    # translate name to equivalent class
    haystack = name.translate(transtable)
    pattern = '1'*n
    indices = []
    search_start = 0
    while search_start > -1:
        search_start = haystack.find(pattern, search_start)
        if search_start > -1:
            indices.append(search_start)
            search_start += 1

    L = len(haystack)
    pairs = set()
    for i in indices:
        #print i, (0, i+1), (i+n-1, L)
        pairs.update(itertools.product(xrange(0, i+1), xrange(i+n-1, L)))
    #print pairs
    return len(pairs)


if __name__ == '__main__':
    in_file = sys.argv[1]
    out_file = os.path.splitext(in_file)[0] + '.out'
    #print out_file
    output = open(out_file, 'w')

    with open(in_file) as test:
        rounds = int(test.next())
        print rounds, 'rounds'

        for i in xrange(rounds):
            #print 'round', i+1
            name, n = test.next().split()
            n = int(n)

            res = solve(name, n)
            #print res
            output.write("Case #%d: %s\n" % (i+1, res))
            #print

    output.close()
