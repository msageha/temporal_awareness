# -*- coding: utf-8 -*-
import numpy as np

def load_hash(filename):
  word2vec_hash = {}
  with open(filename, "r") as f:
    for line in f:
      line = line.split()
      value = np.array(line[1:], dtype=np.float32)
      word2vec_hash[line[0]] = value

  return word2vec_hash