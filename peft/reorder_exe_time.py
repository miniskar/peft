"""Reorder exe_time to match task_connectivity."""

import argparse
import sys
from collections import OrderedDict
import csv
import os

def reorder(dag_file, exe_file):
    with open(dag_file) as fd:
        dag = fd.readlines()

    task_map = OrderedDict()

    for line in dag:
        line = line.strip()
        col = line.split(',')
        task_map[col[0]] = None

    with open(exe_file) as fd:
        exe = fd.readlines()

    for line in exe:
        col = line.split(',')
        if col[0] in task_map:
            task_map[col[0]] = line.strip()

    print(exe[0].strip())

    for t, v in task_map.items():
        if v is not None:
            print(v)

def main(argv):
    # Parse the arguments
    parser = argparse.ArgumentParser(description="""Reorder exe_time to match task_connectivity.""")
    parser.add_argument("-d", "--dag_file", 
                        help="File containing input DAG to be scheduled. Uses default 10 node dag from Arabnejad 2014 if none given.",
                        type=str, required=True)
    parser.add_argument("-t", "--task_execution_file", 
                        help="File containing execution times of each task on each particular PE. Uses a default 10x3 matrix from Arabnejad 2014 if none given.",
                        type=str, required=True)
    args = parser.parse_args(argv[1:])

    reorder(args.dag_file, args.task_execution_file)

if __name__ == "__main__":
    main(sys.argv)