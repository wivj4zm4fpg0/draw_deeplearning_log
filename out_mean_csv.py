import argparse
from statistics import mean

import pandas as pd

# コマンドライン引数の処理
parser = argparse.ArgumentParser()
parser.add_argument(
    '--input_files', default=None, nargs='*',
    help='input csv files'
)
parser.add_argument(
    '--parameter_name', default='acc-top1', type=str,
    help='a parameter to be compared'
)
parser.add_argument(
    '--output', default=None, type=str,
    help='output name'
)
args = parser.parse_args()

csv_list = []
for input_file in args.input_files:
    csv_list.append(pd.read_csv(input_file, sep=' '))

max_list = []
for csv in csv_list:
    max_list.append(len(csv.index))

value_list = []
for i in range(max(max_list)):
    mean_list = []
    for csv in csv_list:
        mean_list.append(csv[args.parameter_name][i])
    value_list.append(mean(mean_list))

with open(args.output, 'w') as f:
    f.write(f'epoch {args.parameter_name}\n')
    for i, value in enumerate(value_list):
        f.write(f'{i} {value}\n')
