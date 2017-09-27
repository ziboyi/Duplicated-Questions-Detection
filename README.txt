数据集：./data/quora_duplicate_questions.tsv    

使用TensorFlow搭建的模型文件：./models/siamese_cnn.py和./models/siamese_lstm.py    

TensorFlow运行中的输出和模型保存在runs目录中    

请运行create_dataset.py进行预处理并将数据集分割为训练集和测试集    

请从GloVe模型的网站下载预训练的词向量： https://nlp.stanford.edu/projects/glove/    

请运行sh train.sh训练LSTM模型    

在train.py的122行，将SiameseLSTM模型修改为SiameseCNN，然后再次运行sh train.sh可训练CNN模型    

请使用sh eval.sh评估模型的性能，运行之前请修改文件中的RUN参数    

请使用sh tensorboard.sh观察模型在训练过程中的变化情况
