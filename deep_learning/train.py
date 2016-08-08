# -*- coding: utf-8 -*-
# trainingを動かすメインファイル
import sys
import os
from model import CNNModel
from chainer import cuda, Variable, FunctionSet, optimizers, optimizer
import numpy as np
import six
import time
import six.moves.cPickle as pickle

import json
import time 
from count import * #import作る必要あり
import argparse

# ロード 作る必要あり
from loader import *
from load_word2vec import * 

import ipdb # デバッグ用

parser = argparse.ArgumentParser()

parser.add_argument('--train', default='train.ff', help='training file')
parser.add_argument('--test', default='test.ff', help='test file')
parser.add_argument('--model', default='model', help='model file')

parser.add_argument('--gpu', '-g', default=-1, type=int, help='GPU ID (negative value indicates CPU)')
parser.add_argument('--seed', '-s', default=1, type=int, help='seed of random number generator') #seedをどうするか，デフォルトは1

parser.add_argument('--data_size', default=10000, type=int, help='number of training data size') #training data size

parser.add_argument('--batchsize', '-b', default=10, type=int, help='number of minibatch size')
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

parser.add_argument('--classias', default=0.0, type=float, dest = 'classias', help='classias') #classiasで学習した各値をふくめるかどうか．値は倍率

parser.add_argument('--tgt_center', default=False, action = 'store_true', dest = 'tgt_center', help='tgt_center')

args = parser.parse_args()
print args
sys.stdout.flush() #コンソール画面にすぐに出力させるためのもの．
np.random.seed(args.seed)

#argsパラメータを変数に落としこむ
train_path, test_path, model_path = args.train, args.test, args.model

tgt, cform, surface, first, last, classias, tgt_center, tgt_sentence, data_size = args.tgt, args.cform, args.surface, args.first, args.last, args.classias, args.tgt_center, args.tgt_sentence, args.data_size

gpu_flag = False #gpuは使わない

if args.tgt_center:
  MAX_WIDTH = 220
else:
  MAX_WIDTH = 110

filename = "/Volumes/shinolab/word2vec/twitter/tweets.txt"
word2vec_hash = load_hash(filename)

x_train, y_train, z_train, unit_length = load_data(train_path, MAX_WIDTH, word2vec_hash, tgt, cform, surface, first, last, classias, tgt_center, tgt_sentence, data_size)
print "=> {0} train data loaded. train_length = {1}".format(str(train_path), str(len(x_train)) )
print "unit_length = %s" % str(unit_length)
sys.stdout.flush()

x_test, y_test, z_test, _ = load_data(test_path, MAX_WIDTH, word2vec_hash, tgt, cform, surface, first, last, classias, tgt_center, tgt_sentence, data_size)
print "=> {0} test data loaded. test_length = {1}".format(str(test_path), str(len(x_test)) )
sys.stdout.flush()

N_train = len(x_train) #train, testの長さ
N_test = len(x_test)
n_epoch = 100
batchsize = args.batchsize
filters, units_1, drop_ratio, conv_width = args.filters, args.units, args.drop_ratio, args.conv_width

#modelをCNNモデルに設定
model = CNNModel(filters, units_1, unit_length, drop_ratio, conv_width)

# Setup optimizer，最適化手法としてAdamを使う
opt = optimizers.Adam()
opt.setup(model)

if args.decay_rate != 0.0:
    opt.add_hook(optimizer.WeightDecay(args.decay_rate))

cur_at = time.time()
models = []

counter = Counter()

print "epoch, sum_loss_train/N, sum_accuracy_train/N, sum_loss_test, sum_accuracy_test, epoch_time"

for epoch in xrange(1, n_epoch + 1):

  # training 学習
  perm = np.random.permutation(N)
  sum_loss_train = 0
  sum_accuracy_train = 0

  for i in xrange(0, N, batchsize): #0~Nのうちbatchsizeで割りきれる時だけ
    x_batch = x_train[perm[i:i+batchsize]] #iから，i+batchsizeまで，つまりbatchsize分とりだす
    y_batch = y_train[perm[i:i+batchsize]]

    if gpu_flag is True:
      x_batch = cuda.to_gpu(x_batch)
      y_batch = cuda.to_gpu(y_batch)

    opt.zero_grads()
    # ipdb.set_trace()
    system_label, loss, accuracy = model.forward(x_batch, y_batch)
    loss.backward()
    opt.update()
    sum_loss_train += float(cuda.to_cpu(loss.data)) * len(x_batch)
    sum_accuracy_train += float(cuda.to_cpu(accuracy.data)) * len(x_batch)

  #evaluation 評価
  labels = []

  if gpu_flag is True:
    x_test = cuda.to_gpu(x_test) #元のコードだと cuda.to_gpu(x_batch) だったが，間違っていると思う
    y_test = cuda.to_gpu(y_test)

  system_label, loss, accuracy = model.forward(x_test, y_test, train=False)

  sum_loss_test = float(cuda.to_cpu(loss.data)) * len(x_test) / N_test
  sum_accuracy_test = float(cuda.to_cpu(accuracy.data)) * len(x_test) / N_test

  now = time.time()
  print "{0:3d}, {1:.4f}, {2:.4f}, {3:.4f}, {4:.4f}, {5:.2f} sec/ep".format(epoch, sum_loss_train/N, sum_accuracy_train/N, sum_loss_test, sum_accuracy_test, now - cur_at)
  sys.stdout.flush()

  cur_at = now

  # 現在の最もいい学習モデルをシリアライズして，保存する
  # models.append(pickle.dumps(model, -1))
  # if counter.best_count(sum_accuracy_dev, epoch) == args.validation_depth:
  #   print "best epoch is {0:3d}".format(counter.epoch_best_num)
  #   print "best test accucary is {0:.4f} and model file wrote to '{1}'".format(counter.best, model_path)

  #   #モデルの書き出し
  #   f = open(model_path, 'wb')
  #   f.write(models[counter.epoch_best_num])
  #   f.close()

sys.exit()

