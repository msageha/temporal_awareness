# modelのコンバージョンレイヤー1をcsvファイルに書き出すもの
import sys
import os
from train_model import CNNModel
from chainer import cuda, Variable, FunctionSet, optimizers
import numpy as np
import six
import six.moves.cPickle as pickle

import pandas
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--model', default='model',help='model file')
args = parser.parse_args()

model = pickle.load(open(args.model, "rb"))

print pandas.DataFrame(model.conv1.W.data[:,0,0,:]).to_csv()
