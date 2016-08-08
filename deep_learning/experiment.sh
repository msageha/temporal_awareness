
PYTHON=/home/matsuda/workspace/olim/PythonTest/bin/python
decay_rate=(0.001 0.0001)
drop_ratio=(0.0 0.3)
filters=(500 1000 2000) 
units=(4 50 100 150)
conv_width=(2 3 4)
tgt=(--tgt --no-tgt)
cform=(--cform --no-cform)
seed=(2)

file_tmpl="de={1}_dr={2}_f={3}_u={4}_tgt={5}_wd={6}_cf={7}_s={8}"

# mezcal02, mezcal10のみパスワード必要？
servers=6/martini02,6/charanda01,6/charanda02,6/charanda03,6/charanda04,6/tequila,6/vodka
servers2=2/mezcal01,2/mezcal02,2/mezcal03,2/mezcal04,2/mezcal05,2/mezcal06,2/mezcal07,2/mezcal08
servers3=4/mezcal09,4/mezcal10,4/mezcal11,4/mezcal12

# libatlas-base-dev 未インストールの機体たち
servers4=4/mezcal13,4/mezcal14,4/mezcal15,4/mezcal16,4/mezcal17,4/mezcal18,4/mezcal19,4/mezcal20
#ss=${servers},${servers2},${servers3},${servers4}
ss=${servers},${servers2},${servers3}

#sss=${servers2},${servers3},${servers4}
#echo "mkdir -p /work/matsuda; scp martini01:/work/mastuda/300.kct /work/mastuda/300.kct" | /home/matsuda/bin/parallel --onall -S ${sss}

echo "rm -f /work/matsuda/300.*.kct" | /home/matsuda/bin/parallel --onall -S ${ss} --tag

/home/matsuda/bin/parallel --bar --shuf  --nice 10 --sshdelay 10 \
      -S ${ss} --workdir ~/workspace/stepqi2015sango/cnn  \
  "${PYTHON} train.py --train train.ff --test dev.ff --decay_rate {1} --drop_ratio {2} --filters {3} --units {4} {5} --conv_width {6} {7} -s {8} --model models/${file_tmpl} > logs/${file_tmpl}.log; \
${PYTHON} apply_model.py --model models/${file_tmpl} --test test.ff {5} {7} > logs/${file_tmpl}.result" ::: ${decay_rate[@]} ::: ${drop_ratio[@]} ::: ${filters[@]} ::: ${units[@]} ::: ${tgt[@]} ::: ${conv_width[@]} ::: ${cform[@]} ::: ${seed[@]} 
