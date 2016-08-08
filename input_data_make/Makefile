#at marinit01 or martini02 or charanda03 or charanda04

PYTHON=/home/matsuda/sango_env/bin/python
RUBY=ruby #/home/matsuda/.rbenv/shims/ruby

dict/TA.dic: dict/TA.csv
	/opt/local/libexec/mecab/mecab-dict-index -d /home/matsuda/mecab-naist-jdic-0.6.3b-20111013 \
                -u $@ -f utf-8 -t utf-8 $^

#train_test_split:
#	cat ../TA/loose/* | $(RUBY) tweet_sentence_splitter.rb |\
#		 $(RUBY) apply_mecab.rb |\
#		 shuf | $(RUBY) feature_extraction.rb > all.f
#	head -8000 all.f > train.f
#	head -1000 all.f > small.f
#	head -9000 all.f | tail -1000 > dev.f
#	tail -978 all.f > test.f

feature_extraction:
	cat ../annotation/dev.json | $(RUBY) tweet_sentence_splitter.rb |\
		 $(RUBY) apply_mecab.rb |\
		 $(RUBY) feature_extraction.rb > dev.f
	cat ../annotation/train.json | $(RUBY) tweet_sentence_splitter.rb |\
		 $(RUBY) apply_mecab.rb |\
		 $(RUBY) feature_extraction.rb > train.f
	shuf train.f | head -n 1000  > small.f
	cat ../annotation/test.json | $(RUBY) tweet_sentence_splitter.rb |\
		 $(RUBY) apply_mecab.rb |\
		 $(RUBY) feature_extraction.rb > test.f

feature_extraction_withform:
	cat ../annotation/dev.json | $(RUBY) tweet_sentence_splitter.rb |\
		 $(RUBY) apply_mecab.rb |\
		 $(RUBY) feature_extraction.rb -f > dev.ff
	cat ../annotation/train.json | $(RUBY) tweet_sentence_splitter.rb |\
		 $(RUBY) apply_mecab.rb |\
		 $(RUBY) feature_extraction.rb -f > train.ff
	shuf train.ff | head -n 1000  > small.ff
	cat ../annotation/test.json | $(RUBY) tweet_sentence_splitter.rb |\
		 $(RUBY) apply_mecab.rb |\
		 $(RUBY) feature_extraction.rb -f > test.ff

dict/100.txt:
	sort -gr classias.model | grep -v "N" | head -n 100 | cut -f 2  > dict/100.txt

model_small:
	$(PYTHON) train.py --train small.f --test dev.f --model $@ --filters 50 --units 20 --decay_rate 0.0 > logs/small.txt

model_small_cf:
	$(PYTHON) train.py --train small.ff --test dev.ff \
		--model $@ \
		--filters 50 --units 20 --decay_rate 0.0 --cform > logs/small.txt

model_cf:
	$(PYTHON) train.py --train train.ff --test dev.ff \
		--model $@ \
		--filters 800 --units 100 --decay_rate 0.001 --drop_ratio 0.3 \
		--cform --tgt > logs/cf.txt

model_cf_3:
	$(PYTHON) train.py --train train.ff --test dev.ff \
		--model $@ \
		--filters 800 --units 500 --decay_rate 0.001 --drop_ratio 0.0 --conv_width 3 \
		--cform --tgt > logs/cf_3.txt

OPT_FE=--surface --tgt
model_sf_3:
	$(PYTHON) train.py --train train.ff --test dev.ff \
		--model $@ \
		--filters 200 --units 10 --decay_rate 0.0001 --drop_ratio 0.0 --conv_width 3 \
		$(OPT_FE) > sf_3.log
	$(PYTHON) apply_model.py --model $@ --test test.ff $(OPT_FE) > sf_3.result

model_small_mizuki:
	$(PYTHON) mizuki-work/train_model_mizuki_edit.py small.f dev.f $@ > log_small_mizuki_edit.txt

model:
	$(PYTHON) train.py --train train.ff --test dev.ff --model $@ --filters 200 --units 50 --tgt --validation_depth 5 > log_large.txt

model_tgt_center:
	$(PYTHON) train.py --train train.ff --test dev.ff --model $@ --filters 200 --units 50 --tgt --tgt_center --validation_depth 10 > log_large.txt

model_all:
	$(PYTHON) train.py --train train.ff --test dev.ff --model $@ --filters 200 --units 50 --tgt --tgt_sentence --tgt_center --first --last --classias --cform --surface --validation_depth 20 > log_large_all.txt

model_tgt_cform_surface:
	$(PYTHON) train.py --train train.ff --test dev.ff --model $@ --filters 200 --units 50 --tgt --cform --surface --validation_depth 20 > log_large.txt

model_first_last_letter:
	$(PYTHON) train.py --train train.ff --test dev.ff --model $@ --filters 200 --units 50 --first --last > log_large.txt

model_tgt_first_last:
	$(PYTHON) train.py --train train.ff --test dev.ff --model $@ --filters 200 --units 50 --first --last --tgt > log_large.txt

model_tgt_first_last_classias:
	$(PYTHON) train.py --train train.ff --test dev.ff --model $@ --filters 200 --units 50 --first --last --tgt --classias --validation_depth 20 > log_large.txt

model_basic:
	$(PYTHON) train.py --train train.ff --test dev.ff --model $@ --filters 200 --units 50 --decay_rate 0.0 > logs/basic.txt

model_tgt:
	$(PYTHON) train.py --train train.ff --test dev.ff --model $@ --filters 200 --units 50 --tgt --decay_rate 0.0 > logs/tgt.txt

model_basic_d:
	$(PYTHON) train.py --train train.ff --test dev.ff --model $@ --filters 200 --units 50 --decay_rate 0.001 > logs/basic_d.txt

model_tgt_d:
	$(PYTHON) train.py --train train.ff --test dev.ff --model $@ --filters 200 --units 50 --tgt --decay_rate 0.001 > logs/tgt_d.txt

model_basic_d_nodrop:
	$(PYTHON) train.py --train train.ff --test dev.ff --model $@ --filters 200 --units 50 --decay_rate 0.001 --drop_ratio 0.0 > logs/basic_d_nodrop.txt

model_tgt_d_nodrop:
	$(PYTHON) train.py --train train.f --test dev.f --model $@ --filters 200 --units 50 --tgt --decay_rate 0.001 --drop_ratio 0.0 > logs/tgt_d_nodrop.txt

# baseline model : Maximum entropy classifier with bag-of-words features
baseline_model:
	sed -e "s/\t/ /g" < train.f | cut -d ' ' -f2 --complement | egrep -v '^(O|#)' > train.classias
	sed -e "s/\t/ /g" < dev.f | cut -d ' ' -f2 --complement | egrep -v '^(O|#)' > dev.classias
	sed -e "s/\t/ /g" < test.f | cut -d ' ' -f2 --complement | egrep -v '^(O|#)' > test.classias
	classias-train -m classias.model train.classias
	classias-tag -qt -m classias.model < dev.classias
	classias-tag -qt -m classias.model < test.classias

baseline_model_mizuki:
	sed -e "s/\t/ /g" < train.f | cut -d ' ' -f2 --complement | egrep -v '^(O|#)' > train.classias
	sed -e "s/\t/ /g" < dev.f | cut -d ' ' -f2 --complement | egrep -v '^(O|#)' > dev.classias
	sed -e "s/\t/ /g" < test.f | cut -d ' ' -f2 --complement | egrep -v '^(O|#)' > test.classias
	classias-train -m classias.model train.classias
	classias-tag -qt -m classias.model < dev.classias
	classias-tag -t -m classias.model < test.classias > classias.rabel
	$(PYTHON) baseline_result_format.py --classias classias.rabel --test test.classias > classias.result 

# I got following results:
#
# for dev set:
#
#Accuracy: 0.6340 (634/1000)
#Performance by label (#match, #model, #ref) (precision, recall, F1):
#    Z: (118, 199, 177) (0.592965, 0.666667, 0.62766)
#    P: (124, 201, 207) (0.616915, 0.599034, 0.607843)
#    F: (117, 171, 185) (0.684211, 0.632432, 0.657303)
#    N: (271, 423, 389) (0.640662, 0.696658, 0.667488)
#    O: (4, 6, 42) (0.666667, 0.0952381, 0.166667)
#Micro P, R, F1: 0.6340 (634/1000), 0.6340 (634/1000), 0.6340
#Macro P, R, F1: 0.6403, 0.5380, 0.5454
#
# for test set: 
#
#classias-tag -qt -m classias.model < test.classias
#Accuracy: 0.6440 (644/1000)
#Performance by label (#match, #model, #ref) (precision, recall, F1):
#    Z: (129, 214, 199) (0.602804, 0.648241, 0.624697)
#    P: (116, 177, 196) (0.655367, 0.591837, 0.621984)
#    F: (108, 161, 182) (0.670807, 0.593407, 0.629738)
#    N: (285, 436, 390) (0.65367, 0.730769, 0.690073)
#    O: (6, 12, 33) (0.5, 0.181818, 0.266667)
#Micro P, R, F1: 0.6440 (644/1000), 0.6440 (644/1000), 0.6440
#Macro P, R, F1: 0.6165, 0.5492, 0.5666

clean:
	rm *.f
	rm *.classias
	rm classias.model

clean_experiment:
	rm logs/*
	rm /work/matsuda/300.*.kct
	rm models/*
