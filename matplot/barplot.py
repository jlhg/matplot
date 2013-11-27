#!/usr/bin/env python

import argparse
import matplotlib.pyplot as plt
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True,
                        help='input file')
    parser.add_argument('-o', required=True,
                        help='output file')
    parser.add_argument('-xlab',
                        help='label to the x-axis')
    parser.add_argument('-xticks-rotation',
                        help='rotation to the x-ticks'
                        '[angle in degrees|"vertical"|"horizontal"]')
    parser.add_argument('-ylab',
                        help='label to the y-axis')
    parser.add_argument('-title',
                        help='title to the axes')
    parser.add_argument('-fcolor',
                        help='color of the bar faces, scalar or array-like'
                        '[single letter|html hex string|float in the 0-1]')
    parser.add_argument('-fwidth', default='0.8',
                        help='width of the bars, scalar or array-like')
    parser.add_argument('-ecolor',
                        help='color of the bar edges, scalar or array-like'
                        '[single letter|html hex string|float in the 0-1]')
    parser.add_argument('-ewidth',
                        help='width of the bar edges, scalar or array-like')

    args = parser.parse_args()

    x_values = []
    y_values = []

    max_y_value = 0
    times = 0
    with open(args.i, 'r') as fi:
        for line in fi:
            line = line.strip()
            if line == '' or line.startswith('#'):
                continue
            data = line.split('\t')
            x_values.append(data[0])
            y = [float(i) for i in data[1:]]
            ymax = max(y)
            if ymax > max_y_value:
                max_y_value = ymax
            y_values.append(y)
            times = len(y)

    bar_kwargs = {
        'align': 'center',
    }

    if args.fcolor:
        if len(args.fcolor.split(' ')) > 1:
            fcolors = args.fcolor.split(' ')
        else:
            fcolors = args.fcolor
        bar_kwargs.update({'color': fcolors})

    if args.fwidth:
        if len(args.fwidth.split(' ')) > 1:
            fwidths = [float(i) for i in args.fwidth.split(' ')]
        else:
            fwidths = float(args.fwidth)
        bar_kwargs.update({'width': fwidths})

    if args.ecolor:
        if len(args.ecolor.split(' ')) > 1:
            ecolors = args.ecolor.split(' ')
        else:
            ecolors = args.ecolor
        bar_kwargs.update({'edgecolor': ecolors})

    if args.ewidth:
        if len(args.ewidth.split(' ')) > 1:
            ewidths = [float(i) for i in args.ewidth.split(' ')]
        else:
            ewidths = float(args.ewidth)
        bar_kwargs.update({'width': ewidths})

    plt.subplots()
    # plt.figure(figsize=(5, 15))

    index = np.arange(len(x_values))
    first = True
    for i in range(times):
        if first:
            first = False
        else:
            index = index + fwidths
        plt.bar(index, [x[i] for x in y_values], **bar_kwargs)

    xticks_kwargs = {}

    if args.xticks_rotation:
        xticks_kwargs.update({'rotation': args.xticks_rotation})
        xticks_kwargs.update({'horizontalalignment': 'right'})

    plt.xticks(*[index - fwidths, x_values], **xticks_kwargs)
    plt.ylim(0, max_y_value * 1.2)

    if args.xlab:
        plt.xlabel(args.xlab)
    if args.xlab:
        plt.ylabel(args.ylab)
    if args.title:
        plt.title(args.title)

    plt.tight_layout()
    plt.savefig(args.o)


if __name__ == '__main__':
    main()
