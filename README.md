# Duplicated Questions Detection

For more information, please see this [post](https://ziboyi.github.io/Project-Duplicated-Questions-Detection/)

The dataset is ./data/quora_duplicate_questions.tsv, you may download it from https://data.quora.com/First-Quora-Dataset-Release-Question-Pairs

The networks use TensorFlow r0.12: ./models/siamese_cnn.py and ./models/siamese_lstm.py    

The models trained by neural networks are stored in ./runs

Run create_dataset.py to preprocess dataset and split it to training and testing set.

The word vector is downloaded from: https://nlp.stanford.edu/projects/glove/    

Run train.sh to train LSTM model.

In line 122 of train.py，modify SiameseLSTM to SiameseCNN and run train.sh again if you want to train CNN model.

Run eval.sh to evaluate the models' performance. Note that the "RUN" parameter in this file indicates which model will be evaluateed.

Running tensorboard.sh will shows the loss function during training.
