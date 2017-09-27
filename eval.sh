#!/bin/bash

RUN="1491655385" #baseline NN
RUN="1491735741" #LSTM

vectors="glove.6B.100d.txt"
#vectors="./glove.twitter.27B/glove.twitter.27B.200d.txt"

test_data="./data/test.full.tsv"
#test_data="./Quora_question_pair_partition/test.tsv"

# tensorboard --logdir ./runs/${RUN}/summaries/
python eval.py \
    --test_data_file="${test_data}" \
    --checkpoint_dir="runs/${RUN}/checkpoints" \
    --embeddings_file="${vectors}"
