"""Merge the init time with the compute time."""

import argparse
import sys
from collections import OrderedDict
import csv
import os

def reorder(exe_file, init_comm_file):
    with open(init_comm_file) as fd:
        init_comm = fd.readlines()

    init_map = {} 

    for line in init_comm:
        line = line.strip()
        col = line.split(',')
        init_map[col[0]] = col[1]

    with open(exe_file) as fd:
        exe = fd.readlines()

    for line in exe:
        col = line.split(',')
        if col[0].strip() in init_map:
            for i in range(1, len(col)):
                col[i] = col[i].strip()
                if col[i] != "inf":
                    col[i] = int(col[i])
                    col[i] += int(init_map[col[0]])
            print(', '.join(map(str, col)))
        else:
            print(line, end='')

def main(argv):
    # Parse the arguments
    parser = argparse.ArgumentParser(description="""Reorder exe_time to match task_connectivity.""")
    parser.add_argument("-t", "--task_execution_file", 
                        help="File containing execution times of each task on each particular PE. Uses a default 10x3 matrix from Arabnejad 2014 if none given.",
                        type=str, required=True)
    parser.add_argument("-i", "--init_comm_file",
                        help="File containing the initial communication overhead inrrespective of which processor it is run on.",
                        type=str, required=True)
    args = parser.parse_args(argv[1:])
    reorder(args.task_execution_file, args.init_comm_file)

if __name__ == "__main__":
    main(sys.argv)