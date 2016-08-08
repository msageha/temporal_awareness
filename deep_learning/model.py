# -*- coding: utf-8 -*-
# モデルを適用していくファイル．
import time
import numpy as np
from chainer import cuda, Variable, FunctionSet, optimizers
import chainer.functions as F

import ipdb

class CNNModel(FunctionSet):
  def __init__(self, n_filters=200, n_units_1=50, drop_ratio=0.5, conv_width=2, unit_length=100):
    self.vec_len=unit_length
    self.conv_width = conv_width * self.vec_len
    self.n_filters=n_filters
    self.n_units_1 = n_units_1
    self.drop_ratio=drop_ratio
    super(CNNModel, self).__init__(
      conv1 = F.Convolution2D(1, n_filters, (1,self.conv_width), stride=(1,self.vec_len)), #入力，出力，コンボリューションの長さ，スライド
      l2 = F.Linear(n_filters, n_units_1),
      lo = F.Linear(n_units_1, 4)
    )

  def forward(self, x_data, y_data, train=True, gpu=-1):

    if gpu >= 0:
      x_data = cuda.to_gpu(x_data)
      y_data = cuda.to_gpu(y_data)

    # ipdb.set_trace()
    x, t = Variable(x_data), Variable(y_data)
    # tanhを適用しているけど，sigmoidのほうがいいかも？
    h1 = F.max(F.tanh(self.conv1(x)), axis=3, keepdims=True)
    # h2 = F.max(F.sigmoid(self.conv2(x2)), axis=3, keepdims=True)
    h = F.dropout(F.sigmoid(self.l2(h1)), train=train, ratio=self.drop_ratio)
    y = self.lo(h)
    return y,F.softmax_cross_entropy(y, t), F.accuracy(y,t)

# class CNNModel(FunctionSet):
#     def __init__(self, n_vocab=1000, n_units=25, train=True, ratio=0.5, conv_width=3, unit_length=100):
#         super(ConvolutionEncoder, self).__init__(
#             n_vocab=n_vocab, n_emb=n_emb, train=train,ratio=ratio
#         )
#         self.conv_width = conv_width
#         self.vec_len = unit_length
#         self.n_filters = n_units
#         self.n_units   = n_units
#         #print(n_units, n_emb)
#         self.add_link('conv1',L.Convolution2D(1, self.n_filters, (self.conv_width, self.unit_length), stride=(1, self.unit_length), use_cudnn=False))
#         #self.to_init.append(self.conv1)
#         #self.add_link('conv1',L.Convolution2D(1, self.n_filters, (self.conv_width, n_units), stride=(1, n_units), use_cudnn=False))

#     def forward(self, x_data, y_data, train=True, gpu=-1):
#         batchsize=10
#         e = F.dropout(self.embed(chainer.Variable(sequence)), train=train)
#         # shape が,(sequence length, batchsize, vectorlength) になっていたので、
#         # swapaxes で(batchsize, sequence length, vectorlength) に修正
#         e = F.swapaxes(e,0,1)
#         #print(e.data.shape)
#         #e = F.reshape(e, (batchsize, 1, len(sequence), self.vec_len))
#         e = F.reshape(e, (batchsize, 1, len(sequence), self.vec_len))
#         e = F.tanh(e)
#         c = self.conv1(e)
#         h = F.reshape(F.max(c, axis=2), (batchsize, self.n_filters))
#         return h