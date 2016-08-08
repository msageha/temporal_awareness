# -*- coding: utf-8 -*-
require "oj"

require 'strscan'

require_relative "../lib/sentence_splitter.rb"

class TweetSentenceSplitter
  
  SENTENCE_SEPARATORS = ['。　?', '．　?', '？　?', '！　?']
  SENTENCE_REGEXP = Regexp.compile(".*?(?:" + SENTENCE_SEPARATORS.join("|") + ")", Regexp::MULTILINE)
  
  def initialize()
    @ss = SentenceSplitter.new
  end
  
  def sentence_split(sentence)
    ret = []
    ss = StringScanner.new(sentence)
    while sent = ss.scan(SENTENCE_REGEXP)
      ret << sent.gsub("　","").gsub("\n","").strip
    end
    ret << ss.rest
    
    return ret.map{|e| e.strip}.reject{|e|
      e.length == 1
    }
  end
  
  def do(json_string)
    obj = Oj.load(json_string)
    #obj["texts"] = sentence_split(obj["text"])
    obj["texts"] = @ss.split(obj["text"].to_s.gsub(" ","　"))
    #json["text"]
    #return obj.to_json
    return Oj.dump(obj)
  end
end

if __FILE__ == $0
  # 一行1エントリの
  s = TweetSentenceSplitter.new()
  while line = gets()
    puts s.do(line)
  end
end
