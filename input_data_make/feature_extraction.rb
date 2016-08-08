# -*- coding: utf-8 -*-
require 'oj'

class FeatureExtractorContainer
  def initialize
    # 個々の素性抽出機が入る
    @extractors = []
  end
  def register(fe)
    @extractors << fe
  end
  def do(obj)
    return @extractors.map { |fe|
      fe.do(obj)
    }.uniq
  end
  def [](i)
    return @extractors[i]
  end
end

class FeatureExtractorBase
  def generate_feature_string(label = "true", val=1.0)
    return "#{label.gsub(/\n/,'NL')}" if val == 1.0
    return "#{label.gsub(/\n/,'NL')}:#{val}"
  end
  alias :gfs :generate_feature_string
  def do(token_array)
    raise NotImprementedError
  end
  def category
    return ''
  end
end

# unigram素性を抽出するextractor
class UnigramFeature < FeatureExtractorBase
  def category; 'u'; end
  def do(obj)
    ret = []
    obj['mecab'].each  do |sentence|  # 各文
      sentence.each do |token| # 各トークン
        ret << token[0]
      end
    end
    return ret
  end
end

class BigramFeature < FeatureExtractorBase
  def category; 'bi'; end
  def do(obj)
    ret = []
    obj['mecab'].each  do |sentence|  # 各文
      sentence.each_slice(2) do |t1,t2| # 各トークン
        next unless t1
        next unless t2
        ret << [t1[0],t2[0]].join("_")
      end
    end
    return ret
  end
end

class CFormFeature < FeatureExtractorBase
  def category; 'cf'; end
  def do(o)
    ret = []
    o['mecab'].each do |sentence|
      sentence.each do |token|
        ret << [token[7], token[6]].join("_") if token[6] != "*"
      end
    end
    return ret
  end
end

class KeywordDistanceFeature
  WINDOW_SIZE = 4
  def category; 'dist';end
  def do(o)
    kw = o['TA_t']
    ret = []
    o['mecab'].each do |sentence|
      sentence.each.with_index do |token, idx|
        if token[0] == kw
          (-WINDOW_SIZE..WINDOW_SIZE).each do |offset|
            next if idx+offset < 0
            begin
              ret << ["kw[#{offset}]", sentence[idx+offset][0] ].join("_") 
            rescue
              #STDERR.puts $!, sentence, token
              next
            end
          end
        end
      end
    end
    return ret    
  end
end

class UnigramWithCForm < FeatureExtractorBase
  def category; "hoge"; end
  def do(o)
    ret = []
    target_num = 0
    o["mecab"].each_with_index do |sentence, i|
      tgt_flag = 0
      sentence.each_with_index do |token, j|
        if token[0] == o["TA_t"]
         tgt_flag = 1
        end
        t = token[0].gsub("@@@", "")
	if j == sentence.length-1 then
	  j = -1
	end
        ret << "#{token[0]}@@@#{token[6]}@@@#{i}@@@#{j}@@@#{tgt_flag}"
      end
    end
    return ret
  end
  def target_num(o)
    o["mecab"].each_with_index do |sentence, i|
      sentence.each_with_index do |token, j|
        if token[0] == o["TA_t"]
          return i
        end
      end
    end
    return 0
  end
end

# renderer
class FeatureVectorRendererForClassias
  def render(features, label=nil)
    return [label, features.join(" ")].join(" ")
  end
end

class FeatureVectorRendererForClassiasWithComment
  def render(features, label=nil, comment=nil)
    return ["# #{comment}", [label, features.join(" ")].join(" ")].join("\n")
  end  
end

class FeatureVectorRendererForClassiasWithCommentWithTarget
  def render(features, label=nil, target_num = nil, comment=nil, target=nil)
    return ["# #{comment}", [label, target, target_num, features.join(" ")].join("\t")].join("\n")
  end  
end

@fe = FeatureExtractorContainer.new()

require 'optparse'
params = ARGV.getopts("uf")

## 素性抽出機にモジュールを登録する
if params["f"]
  # 27 way
  @fe.register(UnigramWithCForm.new())
else
  @fe.register( UnigramFeature.new() )
end
#@fe.register( BigramFeature.new() )
#@fe.register( CFormFeature.new() )
#@fe.register( KeywordDistanceFeature.new() )

## レンダラ
#@renderer = FeatureVectorRendererForClassias.new()
#@renderer = FeatureVectorRendererForClassiasWithComment.new()
@renderer = FeatureVectorRendererForClassiasWithCommentWithTarget.new()

while line = gets()
  obj = Oj.load(line.chomp)
  target_num = @fe[0].target_num(obj)
  features = @fe.do(obj)
  #puts target_num
  #line = @renderer.render(features, obj["TA_loose"], obj["text"].gsub("\n", ""))
  line = @renderer.render(features, obj["TA_gold"], target_num, obj["text"].to_s.gsub("\n", ""), obj["TA_t"])
  puts line
end
