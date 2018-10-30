import argparse
import os
import shutil

parser = argparse.ArgumentParser(description='move script')
parser.add_argument(
    '-i', '--input_dirs', default=None, nargs='*', help='input files'
)
parser.add_argument(
    '-o', '--output_dir', default=None, type=str, help='output file'
)

args = parser.parse_args()

assert os.path.isdir(args.output_dir)

for input_file in args.input_dirs:
    train_path = os.path.join(input_file, 'train.log')
    val_path = os.path.join(input_file, 'val.log')
    assert os.path.exists(train_path) and os.path.exists(val_path)
    output_path = os.path.join(args.output_dir, os.path.basename(input_file))
    os.makedirs(output_path, exist_ok=True)
    shutil.copy(train_path, output_path)
    shutil.copy(val_path, output_path)
