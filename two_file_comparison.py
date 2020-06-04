# 2つのcsvファイルを読み込んで精度などを比較するスクリプト

import argparse

import matplotlib.pyplot as plt
import pandas as pd

# コマンドライン引数の処理
parser = argparse.ArgumentParser()
parser.add_argument('input_file_1', default=None, type=str, help='input train file')
parser.add_argument('input_file_2', default=None, type=str, help='input validation file')
parser.add_argument('-n1', '--name_1', default='train', type=str, help='first graph name')
parser.add_argument('-n2', '--name_2', default='validation', type=str, help='second graph name')
parser.add_argument('-pn', '--parameter_name', default='acc-top1', type=str, help='a parameter to be compared')
parser.add_argument('-dx', '--delimiter_x', default=25, type=int, help='units to break graphs')
parser.add_argument('-dy', '--delimiter_y', default=25, type=int, help='units to break graphs')
parser.add_argument('-yam', '--y_axis_max', default=None, type=int, help='y axis max size')
parser.add_argument('-yn', '--y_name', default='accuracy(%)', type=str, help='name of the y axis of the graph')
parser.add_argument('-xn', '--x_name', default='epoch', type=str, help='name of the x axis of the graph')
args = parser.parse_args()

# csvファイルの読み込み
file1 = pd.read_table(args.input_file_1)
file2 = pd.read_table(args.input_file_2)

# 比較するパラメータ
# ここで作ったリストがグラフ描画に使われる
file1_acc_list = []
file2_acc_list = []

# epoch数 少ない方を優先する
epoch_length = min(len(file1), len(file2))

# 精度が0~1の間になっているので0~100に正規化する
for i in range(epoch_length):
    file1_acc_list.append(file1[args.parameter_name][i] * 100)
    file2_acc_list.append(file2[args.parameter_name][i] * 100)

x = list(range(1, epoch_length + 1))  # グラフのx軸の設定

max_value = max(max(file1_acc_list), max(file2_acc_list))  # ２つのリストの最大値を取得
if args.y_axis_max:
    y_axis_max = args.y_axis_max
elif max_value >= 100:
    y_axis_max = 100
else:
    # ２桁の数値の２の位に１を足して１０を掛けることによりy軸の最大値を決定する
    y_axis_max = ((int('{0:02d}'.format(int(max_value))[0]) + 1) * 10)

plt.plot(x, file1_acc_list, label=args.name_1)
# 破線で割り当てる
plt.plot(x, file2_acc_list, linestyle='--', label=args.name_2)
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
