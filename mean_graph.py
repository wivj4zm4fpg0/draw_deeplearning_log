import argparse

import matplotlib.pyplot as plt
import pandas as pd
from statistics import mean

# コマンドライン引数の処理
parser = argparse.ArgumentParser()
parser.add_argument(
    '-tf', '--train_files', default=None, nargs='*',
    help='input csv files'
)
parser.add_argument(
    '-vf', '--val_files', default=None, nargs='*',
    help='input csv files'
)
parser.add_argument(
    '-tn', '--train_name', default=None, nargs='*',
    help='graph names'
)
parser.add_argument(
    '-vn', '--val_name', default=None, nargs='*',
    help='graph names'
)
parser.add_argument(
    '-pn', '--parameter_name', default='acc-top1', type=str,
    help='a parameter to be compared'
)
parser.add_argument(
    '-dx', '--delimiter_x', default=25, type=int,
    help='units to break graphs'
)
parser.add_argument(
    '-dy', '--delimiter_y', default=25, type=int,
    help='units to break graphs'
)
parser.add_argument(
    '-yam', '--y_axis_max', default=None, type=int,
    help='y axis max size'
)
parser.add_argument(
    '-yn', '--y_name', default='accuracy(%)', type=str,
    help='name of the y axis of the graph'
)
parser.add_argument(
    '-xn', '--x_name', default='epoch', type=str,
    help='name of the x axis of the graph'
)
args = parser.parse_args()

assert len(args.train_files) == len(args.val_files)

train_csv_list = []
val_csv_list = []

for i in range(len(args.train_files)):
    train_csv_list.append(
        [pd.read_csv(train_file, sep=' ') for train_file in args.train_files]
    )
    val_csv_list.append(
        [pd.read_csv(val_file, sep=' ') for val_file in args.val_files]
    )

epoch_length = min(
    [len(train_csv) for train_csv in train_csv_list] +
    [len(val_csv) for val_csv in val_csv_list]
)

train_value_list = []
val_value_list = []

for i in range(epoch_length):
    train_value_list.append(
        mean([train_value[args.parameter_name][i] for train_value in train_csv_list])
    )
    val_value_list.append(
        mean([val_value[args.parameter_name][i] for val_value in val_csv_list])
    )

x = list(range(1, epoch_length + 1))  # グラフのx軸の設定

max_value = max(max(train_value_list), max(val_value_list))  # ２つのリストの最大値を取得
if args.y_axis_max:
    y_axis_max = args.y_axis_max
elif max_value >= 100:
    y_axis_max = 100
else:
    # ２桁の数値の２の位に１を足して１０を掛けることによりy軸の最大値を決定する
    y_axis_max = ((int('{0:02d}'.format(int(max_value))[0]) + 1) * 10)

plt.plot(x, train_value_list, label=args.train_name)
# 破線で割り当てる
plt.plot(x, val_value_list, linestyle='--', label=args.val_name)
plt.legend()  # グラフのラベル名を図に表示する

plt.xlabel(args.x_name)  # x軸の名前を決定する
plt.ylabel(args.y_name)  # y軸の名前を決定する

plt.xlim(0, epoch_length + 1)  # x軸の範囲を指定
plt.ylim(0, y_axis_max)  # y軸の範囲を指定

# グラフのメモリの設定
x_scale = list(range(0, epoch_length + 1, args.delimiter_x))
x_scale[0] = 1  # 最初は1から始まるようにする
plt.xticks(x_scale)  # ここでx軸の目盛りの設定が設定される
# y軸の設定
y_scale = list(range(0, y_axis_max + 1, args.delimiter_y))
plt.yticks(y_scale)

plt.show()  # 図の表示
