#! /usr/bin/env python
# -*- encoding: utf-8 -*-


import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import tensorflow as tf
import numpy as np
import os
import time
import datetime
import data_helpers
from tensorflow.contrib import learn
import csv

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

# Parameters
# ==================================================

# Data Parameters
tf.flags.DEFINE_string("test_data_file", "./data/test.full.tsv", "Data source for the test data.")
tf.flags.DEFINE_string("embeddings_file", "glove.6B.100d.txt", "Data source for the pretrained word embeddings")

# Eval Parameters
tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
tf.flags.DEFINE_string("checkpoint_dir", "", "Checkpoint directory from training run")
tf.flags.DEFINE_boolean("eval_train", False, "Evaluate on all training data")

# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")


FLAGS = tf.flags.FLAGS
FLAGS._parse_flags()
print("\nParameters:")
for attr, value in sorted(FLAGS.__flags.items()):
    print("{}={}".format(attr.upper(), value))
print("")

# Load data
print("Loading data...")
q1, q2, y, q1_lengths, q2_lengths = data_helpers.load_data_and_labels(FLAGS.test_data_file)
x_raw = q1 + q2

# Build vocabulary
vocab_path = os.path.join(FLAGS.checkpoint_dir, "..", "vocab")
vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
x_test = np.array(list(vocab_processor.transform(x_raw)))

x1_test = x_test[:len(q1)]
x2_test = x_test[len(q1):]
y_test = np.argmax(y, axis=1)


print("\nEvaluating...\n")

# Evaluation
# ==================================================
checkpoint_file = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
graph = tf.Graph()
with graph.as_default():
    session_conf = tf.ConfigProto(
      allow_soft_placement=FLAGS.allow_soft_placement,
      log_device_placement=FLAGS.log_device_placement)
    sess = tf.Session(config=session_conf)
    with sess.as_default():
        # Load the saved meta graph and restore variables
        saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
        saver.restore(sess, checkpoint_file)

        # Get the placeholders from the graph by name
        input_x1 = graph.get_operation_by_name("input_x1").outputs[0]
        input_x2 = graph.get_operation_by_name("input_x2").outputs[0]
        # input_y = graph.get_operation_by_name("input_y").outputs[0]
        dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]
        input_x1_length = graph.get_operation_by_name("input_x1_length").outputs[0]
        input_x2_length = graph.get_operation_by_name("input_x2_length").outputs[0]

        # Tensors we want to evaluate
        predictions = graph.get_operation_by_name("output/predictions").outputs[0]

        # Generate batches for one epoch
        batches = data_helpers.batch_iter(list(zip(x1_test, x2_test, q1_lengths, q2_lengths)), FLAGS.batch_size, shuffle=False)

        # Collect the predictions here
        all_predictions = []

        for batch in batches:
            x1_batch, x2_batch, x1_length_batch, x2_length_batch = zip(*batch)
            batch_predictions = sess.run(predictions, {
                input_x1: x1_batch,
                input_x2: x2_batch,
                dropout_keep_prob: 1.0,
                input_x1_length: x1_length_batch,
                input_x2_length: x2_length_batch
            })
            all_predictions = np.concatenate([all_predictions, batch_predictions])

# Print accuracy if y_test is defined
if y_test is not None:
    correct_predictions = float(sum(all_predictions == y_test))

    labels = [0, 1]
    precision = precision_score(y_test, all_predictions, labels)
    recall = recall_score(y_test, all_predictions, labels)
    f1 = f1_score(y_test, all_predictions, labels)

    print("Total number of test examples: {}".format(len(y_test)))
    print("Accuracy: {:.4f}".format(correct_predictions/float(len(y_test))))
    print("Precision: {:.4f}".format(precision))
    print("Recall: {:.4f}".format(recall))
    print("F1: {:.4f}".format(f1))

# Save the evaluation to a csv
predictions_human_readable = np.column_stack((np.array(q1), np.array(q2), [int(x) for x in all_predictions], np.array(y_test)))
out_path = os.path.join(FLAGS.checkpoint_dir, "..", "prediction.csv")
print("Saving evaluation to {0}".format(out_path))
with open(out_path, 'w') as f:
    csv.writer(f, delimiter='\t').writerows(predictions_human_readable)
