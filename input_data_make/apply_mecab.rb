#require 'MeCab'

if RUBY_PLATFORM == "x86_64-linux"
  require 'mecab'
else
  require 'MeCab'
end

require 'oj'

@mecab = MeCab::Tagger.new("-u dict/TA.dic")
while line = gets()
  obj = Oj.load(line)
  obj["mecab"] = obj["texts"].map do |sentence|
    offset = 0
    ret = []
    @mecab.parse(sentence).each_line do |l|
      #puts l
      a = l.chomp.split("\t")
      next if a.first.start_with?("EOS")
      a[1] = a[1].split(",")
      a << offset
      a << offset + a.first.length - 1
      offset += a.first.length
      #ret << a.join("\t") unless a.first.match("EOS")
      ret << a.flatten
    end
    ret#.join("\n")
  end
  puts Oj.dump(obj)
end
