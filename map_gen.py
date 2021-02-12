#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random


def map_gen(x, y, density):
    print('{}.ox'.format(y))
    lines = []
    for i in range(int(y)):
        line = []
        for j in range(int(x)):
            if (random.randint(0, int(y)) * 2) < int(density):
                line.append('o')
            else:
                line.append('.')
        lines.append(''.join(line))
    print('\n'.join(lines))


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Missing parameters.')
        exit()
    map_gen(*sys.argv[1:4])
