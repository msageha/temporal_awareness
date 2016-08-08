require 'kyotocabinet'
include KyotoCabinet

to_filename = ARGV.shift
from_filename = ARGV.shift

db = DB::new()
unless db.open(to_filename, DB::OWRITER | DB::OCREATE)
  STDERR.puts()
end

open(from_filename).each.with_index do |line,idx|
  puts idx if idx % 10000 == 0
  begin
    arr = line.chomp.split(" ")
  rescue
    next
  end
  next if arr.length < 5
  key = arr.shift
  val = arr.map(&:to_f)
  #puts key, val.inspect
  db.set(key,val)
end

