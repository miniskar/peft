"""Convert dep files into task_connectivity.csv"""

import argparse
import sys
from collections import OrderedDict
import csv
import os

def convert_dep(filename, weight):
    print(filename)
    with open(filename) as fd:
        dep = fd.readlines()

    dep_map = OrderedDict()
    
    for line in dep:
        line = line.strip()
        layer, depends = line.split(':')
        d = depends.split(',')
        dep_map[layer] = [i.strip() for i in d]

    # Reverse the map from a backwards dependency map to a forwards DAG graph.
    w_map = OrderedDict()
    for k in dep_map.keys():
        w_map[k] = []
        for i, v in dep_map.items():
            if k in v:
                w_map[k].append(i)

    keys = w_map.keys()
    csv_filename = os.path.splitext(filename)[0]+'_task_connectivity.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['T'] + list(keys)
        writer = csv.DictWriter(csvfile, fieldnames, restval='0')
        writer.writeheader()

        for key, value in w_map.items():
            d = {v.strip():weight for v in value if v.strip()}
            print(d)
            d['T'] = key
            writer.writerow(d)

def main(argv):
    # Parse the arguments
    parser = argparse.ArgumentParser(description="""Convert dep files into task_connectivity.csv""")
    parser.add_argument('dep_file', type=str, nargs=1, help='The dep file to convert')
    parser.add_argument('-w', '--weight', type=int, default=3, help='Communication weight')
    args = parser.parse_args(argv[1:])

    convert_dep(args.dep_file[0], args.weight)

if __name__ == "__main__":
    main(sys.argv)