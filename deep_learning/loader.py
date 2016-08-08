# -*- coding: utf-8 -*-
# 今回の実験にてファイルをロードしてベクトルを返すもの．
import sys
import os
import numpy as np
import json

import ipdb

# ラベル周り
labels = {
  "N" : 0,
  "P" : 1,
  "Z" : 2,
  "F" : 3
}

rev_labels = {
  0 : "N",
  1 : "P",
  2 : "Z",
  3 : "F"
}

N = 100 #word2vecの単語ベクトルの長さ

def convert_rev_label(label):
  return rev_labels[label]

def convert_label(label):
  return labels[label]

def get_vector(w, word2vec_hash): #これ何のため？
  v = word2vec_hash.get(w)
  if v == None:
    return np.zeros(N)
  if len(v) != N: #コードではnot equarlだったが，間違っている気が…
    return np.zeros(N)
  return v

# cform周り
import collections
import json
import pprint

def load_cform(filename):
  word2id = collections.defaultdict(lambda: len(word2id))
  with open(filename, "r") as file:
    for line in file:
      f = str(line.rstrip())
      word2id[f]
  return json.loads(json.dumps(word2idm, ensure_ascii=False))

def get_cform_vector(dic, cform, num):
  vec = [0.] * len(dic)
  cf = unicode(cform)
  try:
    vec[dic[cf]] = num
  except KeyError, IndexError:
    print cform
    print json.dumps(dic, ensure_ascii=False)
    sys.stdout.flush()
  return vec

# surface周り
def get_surface_vector(dic, surface, num):
  vec = [0.] * len(dic)
  sf = unicode(surface)
  try:
    vec[dic[sf]] = num
  except KeyError, IndexError:
    pass
  return vec

# classiasまわり
def load_hash(filename):
  future, past, present, non_tense = {}, {}, {}, {}
  with open(filename, "r") as f:
    i = 0
    for line in f: #このあと，インデント確認する必要あり,その他いろいろと確認
      if i < 5:
        i += 1
        continue
    ary = str(line.rstrip()).split()
  if ary[2] == "F":
    future[ary[1]] = float(ary[0])
  elif ary[2] == "Z":
    present[ary[1]] = float(ary[0])
  elif ary[2] == "P":
    past[ary[1]] = float(ary[0])
  elif ary[2] == "N":
    non_tense[ary[1]] = float(ary[0])
  return future, present, past, non_tense

def get_classias_vector(dic_hash, classias):
  if not dic_hash.get(classias):
    return 0
  else:
    return dic_hash[classias]

def load_data(filename, max_width, word2vec_hash, tgt_attention=0.0, cform=0.0, surface=0.0, first_letter=0.0, last_letter=0.0, classias=0.0, tgt_center=False, tgt_sentence=0.0, size=None):
  unit_width = N
  idx = 0 #読み込んだ件数

  #ベクトルの長さを調整
  if tgt_attention:
    unit_width += 1
  if cform:
    dic_cform = load_cform("dict/cform.txt")
    unit_width += len(dic_cform)
  if surface:
    dic_surface = load_cform("dict/100.txt")
    unit_width += len(dic_surface)
  if first_letter:
    unit_width += 1
  if last_letter:
    unit_width += 1
  if classias:
    f_hash, z_hash, p_hash, n_hash = load_hash("./classias.model")
    unit_width += 4
  if tgt_sentence:
    unit_width += 1

  max_width *= unit_width

  temp_x, temp_y, temp_z = [], [], []
  with open(filename, "r") as f:
    for line in f:
      if line.startswith("#"):
        temp_z.append(line)
        continue

      idx += 1
      if idx % 100 == 0:
        sys.stdout.write(".")
        sys.stdout.flush()
      if idx % 1000 == 0:
        print " {}".format(idx)

      data = line.rstrip().split("\t")
      label = data[0]

      # Oタグは読み飛ばす
      if label == "O":
        temp_z.pop()
        continue

      target = data[1]
      target_num = int(data[2])
      feature = data[3].split(" ")
      vectors = []
      v_t = get_vector(target, word2vec_hash)

      if tgt_center:
        for n in range(0, 110 - (target_num + 1)):
          vectors.append([0.] * unit_width)

      num_temp = -1 #多分だが，ターゲットの場所の変数
      for items in feature:
        item, cf, sentence_num, word_num, tgt_include = items.split("@@@")[0:5]
        vector = get_vector(item, word2vec_hash)

        num_temp += 1
        if tgt_attention: #tgtの場所に発火
          if(item==target):
            vector.append(tgt_attention)
            num_tgt = num_temp
          else:
            vector.append(0.0)
        # cform 27次元足す
        if cform:
          vector += get_cform_vector(dic_cform, cf, cform)

        # surface 100次元足す
        if surface:
          vector += get_surface_vector(dic_surface, item, surface)

        # 文の先頭，末尾に発火
        if first_letter:
          if(int(word_num) == 0):
            vector.append(first_letter)
          else:
            vector.append(0.)
        if last_letter:
          if(int(word_num) == -1):
            vector.append(last_letter)
          else:
            vector.append(0.)

        # classiasのmodelを追加
        if classias:
          vector.append(get_classias_vector(f_hash, item))
          vector.append(get_classias_vector(z_hash, item))
          vector.append(get_classias_vector(p_hash, item))
          vector.append(get_classias_vector(n_hash, item))

        if tgt_sentence:
          if (int(tgt_include) == 1):
            vector.append(tgt_sentence)
          else:
            vector.append(0.)

        vectors.append(vector)

      if tgt_center:
        for n in range(0, 110 - len(feature) + (target_num + 1)):
          vectors.append([0.] * unit_width)

      # with open("check.txt", "r") as t:
      #   t.writelines("len(vectors)=" + str(len(vectors)) + ",target_num=" + str(num_tgt) + ",len(feature)=" + str(len(feature)) + "\n")
      #   for vector in vectors:
      #     t.writelines(str(vector[300]))
      #     t.writelines(",")
      #   t.writelines("\n")

      # flatten_temp = reduce(lambda x,y: x+y, vectors)
      # pad_width = max_width - len(flatten_temp)
      # if (pad_width < 0):
      #   sys.stderr.write("Error! Word count over!\n")
      #   sys.exit(-1)

      # if tgt_center:
      #   input_vector = np.array(flatten_temp, dtype=np.float32)
      # else:
      #   input_vecotr = np.lib.pad(np.array(flatten_temp, dtype=np.float32), (0, pad_width), 'constant', constant_values=(0.,0.))

      # temp_x.append(input_vector)
      for i in range(len(vectors), 110): #ツイートの最大の長さを110と仮定
        vectors.append(np.zeros(unit_width))

      temp_x.append(vectors)
      temp_y.append(convert_label(label))

  # if size:
  #   temp_x = temp_x[:size]
  #   temp_y = temp_y[:size]
  #   temp_z = temp_z[:size]

  x = np.array(temp_x, dtype=np.float32).reshape(len(temp_x), 1, 1, -1) #長さがlen(temp_x) * ((100*110)) の2次元配列
  y = np.array(temp_y, dtype=np.int32)
  z = np.array(temp_z, dtype=np.str_)
  ipdb.set_trace()

  return x, y, z, unit_width
