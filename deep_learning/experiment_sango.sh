PYTHON=/home/matsuda/sango_env/bin/python
place=(秋葉原 市役所 交差点 病院 清水寺 仙台 渋谷駅 スカイツリー 改札 動物園)

filters=(200 500 1000 2000)
units=(25 50 100 150)

batchsize=(100 200 250 500)
decay_rate=(0.01 0.005 0.001 0.0005)
drop_rate=(0.25 0.5 0.75)

cform=(0.0 0.5 1.0 2.0 5.0)
tgt=(0.0 0.5 1.0 2.0 5.0)
surface=(0.0 0.5 1.0 2.0 5.0)
first=(0.0 0.5 1.0 2.0 5.0)
last=(0.0 0.5 1.0 2.0 5.0)
tgt_sentence=(0.0 0.5 1.0 2.0 5.0)


dir=work_space

echo "executing in-domain experiment"
/home/matsuda/bin/parallel --bar -j 8 "\
				mkdir ./${dir}/filters{1}.units{2}
				mkdir ./${dir}/filters{1}.units{2}/batch{3}.decay{4}.drop{5}
        ${PYTHON} train.py --train train.ff --test dev.ff --model ./${dir}/filters{1}.units{2}/batch{3}.decay{4}.drop{5}/cform{6}.tgt{7}.surface{8}.first{9}.last{10}.sentence{11}.model --filters {1} --units {2} --batchsize {3} --decay_rate {4} --drop_rate {5} --cform {6} --tgt {7} --surface {8} --first {9} --last {10} --tgt_sentence {11} >  ./${dir}/filters{1}.units{2}/batch{3}.decay{4}.drop{5}/cform{6}.tgt{7}.surface{8}.first{9}.last{10}.sentence{11}.log ;\
        ${PYTHON} apply_model.py --test test.ff --model  ./${dir}/filters{1}.units{2}/batch{3}.decay{4}.drop{5}/cform{6}.tgt{7}.surface{8}.first{9}.last{10}.sentence{11}.model  --filters {1} --units {2} --batchsize {3} --decay_rate {4} --drop_rate {5} --cform {6} --tgt {7} --surface {8} --first {9} --last {10} --tgt_sentence {11} > ./${dir}/filters{1}.units{2}/batch{3}.decay{4}.drop{5}/cform{6}.tgt{7}.surface{8}.first{9}.last{10}.sentence{11}.result ;\
    " ::: ${filters[@]} ::: ${units[@]} ::: ${batchsize[@]} ::: ${decay_rate[@]} ::: ${drop_rate[@]} ::: ${cform[@]} ::: ${tgt[@]} ::: ${surface[@]} ::: ${first[@]} ::: ${last[@]} ::: ${tgt_sentence[@]}
