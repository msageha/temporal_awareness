# -*- coding: utf-8 -*-
# モデルを適用するファイル
import sys
import os
from train_model import CNNModel
from chainer import cuda, Variable, FunctionSet, optimizers
import numpy as np
import six
import six.moves.cPickle as pickle
import xmlrpclib as xmlrpc_client

from loader import *

import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--test', default='test.f', help='test file')
parser.add_argument('--model', default='model', help='model file')

parser.add_argument('--gpu', '-g', default=-1, type=int, help='GPU ID (negative value indicates CPU)')
parser.add_argument('--seed', '-s', default=1, type=int, help='seed of random number generator') #seedをどうするか，デフォルトは1

parser.add_argument('--data_size', default=10000, type=int, help='number of training data size') #training data size

parser.add_argument('--batchsize', '-b', default=100, type=int, help='number of minibatch size')
parser.add_argument('--filters', default=200, type=int, help='number of convolution filters')
parser.add_argument('--units', '-u', default=50, type=int, help='number of hidden units')

parser.add_argument('--decay_rate', default=0.001, type=float, help='weight decay rate')
parser.add_argument('--drop_ratio', default=0.5, type=float, help='drop_out_ratio')
parser.add_argument('--validation_depth', default=10, type=int, help='validation_depth')

parser.add_argument('--conv_width', default=2, type=int, help='conv_width') #n-gram

parser.add_argument('--cform', default=0.0, type=float, dest = 'cform', help='cform_attension')

parser.add_argument('--tgt', default=0.0, type=float, dest = 'tgt', help='tgt_attension') #tgtの位置

parser.add_argument('--surface', default=0.0, type=float, dest = 'surface', help='surface_attension') #bag of wardsの手がかり語素性

parser.add_argument('--first', default=0.0, type=float, dest = 'first', help='first_letter') #接頭語，接尾辞素性
parser.add_argument('--last', default=0.0, type=float, dest = 'last', help='last_letter')

parser.add_argument('--tgt_sentence', default=0.0, type=float, dest = 'tgt_sentence', help='tgt_in_sentence') #tgtが含まれた一文に発火

parser.add_argument('--classias', default=0.0, type=float, dest = 'classias',　help='classias') #classiasで学習した各値をふくめるかどうか．値は倍率

parser.add_argument('--tgt_center', default=False, action = 'store_true', dest = 'tgt_center', help='tgt_center')

args = parser.parse_args()
print args
sys.stdout.flush() #コンソール画面にすぐに出力させるためのもの．

if args.tgt_center:
  MAX_WIDTH = 220
else:
  MAX_WIDTH = 110

test_path = args.test

x_test, y_test, z_test, _ = load_data(test_path, MAX_WIDTH, tgt, cform, surface, first, last, classias, tgt_center, tgt_sentence, data_size)
print "=> {0} test data loaded. test_length = {1}".format(str(test_path), str(len(x_test)) )
sys.stdout.flush()

cnn_model = pickle.load(open(args.model, "rb"))
system_label, loss, acc = cnn_model.forward(x_test, y_test, train=False)

print "test acc: {0:.4f}".format(float(acc.data))





