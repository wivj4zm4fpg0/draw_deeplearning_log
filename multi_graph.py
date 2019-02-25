import argparse

import matplotlib.pyplot as plt
import pandas as pd

# コマンドライン引数の処理
parser = argparse.ArgumentParser()
parser.add_argument(
    '--input_files', default=None, nargs='*',
    help='input csv files'
)
parser.add_argument(
    '--names', default=None, nargs='*',
    help='graph names'
)
parser.add_argument(
    '--parameter_name', default='acc-top1', type=str,
    help='a parameter to be compared'
)
parser.add_argument(
    '--delimiter_x', default=25, type=int,
    help='units to break graphs'
)
parser.add_argument(
    '--delimiter_y', default=25, type=int,
    help='units to break graphs'
)
parser.add_argument(
    '--y_axis_max', default=None, type=int,
    help='y axis max size'
)
parser.add_argument(
    '--y_axis_min', default=0, type=int
)
parser.add_argument(
    '--y_name', default='accuracy(%)', type=str,
    help='name of the y axis of the graph'
)
parser.add_argument(
    '--x_name', default='epoch', type=str,
    help='name of the x axis of the graph'
)
parser.add_argument(
    '--out_name', default='sample', type=str,
    help='output name'
)
parser.add_argument(
    '--label_location', default='lower right', type=str
)
parser.add_argument(
    '--font_size', default=18, type=int
)
parser.add_argument(
    '--extension_line_values', default=None, nargs='*',
    help='please values of extension line'
)
parser.add_argument(
    '--skip_number', default=None, nargs='*'
)
args = parser.parse_args()

assert len(args.input_files) == len(args.names)
csv_list = []

plt.rcParams["font.size"] = args.font_size  # フォントサイズを指定

for i in range(len(args.input_files)):
    csv_list.append(pd.read_csv(args.input_files[i], sep=r'\s', engine='python'))

epoch_length = min([len(csv) for csv in csv_list])

value_list = []

for i in range(len(csv_list)):
    value_list.append(
        [csv_list[i][args.parameter_name][j] * 100 for j in range(epoch_length)]
    )

x = list(range(1, epoch_length + 1))  # グラフのx軸の設定

max_value = max([max(values) for values in value_list])  # ２つのリストの最大値を取得
if args.y_axis_max:
    y_axis_max = args.y_axis_max
elif max_value >= 100:
    y_axis_max = 100
else:
    # ２桁の数値の２の位に１を足して１０を掛けることによりy軸の最大値を決定する
    y_axis_max = ((int('{0:02d}'.format(int(max_value))[0]) + 1) * 10)

for i in range(len(value_list)):  # iの値によって色や線の形を変えてグラフを描画する
    if i in list(map(int, args.skip_number)):  # コマンドライン引数で指定した値のときは描画しない
        continue
    elif (i + 1) % 2 == 0:
        plt.plot(x, value_list[i], label=args.names[i], linestyle='dashed',
                 color=plt.rcParams['axes.prop_cycle'].by_key()['color'][i])
    elif (i + 1) % 3 == 0:
        plt.plot(x, value_list[i], label=args.names[i], linestyle='dashdot',
                 color=plt.rcParams['axes.prop_cycle'].by_key()['color'][i])
    else:
        plt.plot(x, value_list[i], label=args.names[i], linestyle='solid',
                 color=plt.rcParams['axes.prop_cycle'].by_key()['color'][i])

plt.legend(loc=args.label_location)  # グラフのラベル名を図に表示する 引数はラベルの位置を指定

plt.xlabel(args.x_name)  # x軸の名前を決定する
plt.ylabel(args.y_name)  # y軸の名前を決定する

plt.xlim(0, epoch_length + 1)  # x軸の範囲を指定
plt.ylim(args.y_axis_min, y_axis_max)  # y軸の範囲を指定

# x軸のグラフのメモリの設定
x_scale = list(range(0, epoch_length + 1, args.delimiter_x))
x_scale[0] = 1  # 最初は1から始まるようにする
plt.xticks(x_scale)  # ここでx軸の目盛りの設定が設定される

# y軸の設定
y_scale = list(range(args.y_axis_min, y_axis_max + 1, args.delimiter_y))
plt.yticks(y_scale)

# 補助線の描画
if args.extension_line_values:
    plt.hlines(list(map(int, args.extension_line_values)), 0, epoch_length + 1,
               "black", linestyles='dashed')

plt.tight_layout()  # これがないとラベルが出力画像からはみ出る
plt.savefig(f'{args.out_name}.png', format='png', dpi=300)  # 高解像度化して保存
plt.savefig(f'{args.out_name}.eps', format='eps')  # epsで保存
plt.show()  # 図の表示
