import csv
from nlp_utils import normalize
from classifier import NaiveBayes
import os, json
import random

def load_existing_model():
    if os.path.exists('model.json'):
        with open('model.json', 'r') as f:
            data = json.load(f)
            nb=NaiveBayes(
              cat_counts=data['cat_counts'],
              word_counts=data['word_counts'],
              vocab=set(data['vocab']),
              total_docs=data['total_docs'],
              total_words=data['total_words']
            )
            return nb
    return None

def build_model():
    if model := load_existing_model():
        return model, None

    data=[]
    filename = 'emails.csv'

    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        for mail_data, is_spam_num in csv_reader:
            cat = 'spam' if int(is_spam_num)==1 else 'ham'
            data.append((normalize(mail_data), cat))
    
    # shuffle rows
    random.shuffle(data)
    
    # train on 80% of rows
    train_data = data[:int(len(data)*0.8)]
    test_data = data[int(len(data)*0.8):]

    # save train and test data in files
    with open('train_data.json', 'w') as f:
        json.dump(train_data, f)
    with open('test_data.json', 'w') as f:
        json.dump(test_data, f)

    nb=NaiveBayes()
    nb.train(train_data)
    print(f"Trained on: {len(train_data)} emails. Model: {nb}")
    return nb, test_data


def test_model(model, test_data):
  print(f"Testing {len(test_data)} emails. model: {model}")
  num_correct_spam = 0
  num_total_spam = 0

  num_correct_ham = 0
  num_total_ham = 0

  for mail_data, cat in test_data:
    predicted_cat = model.predict(mail_data)
    if cat=='spam':
      num_total_spam+=1
      if predicted_cat=='spam':
        num_correct_spam+=1
    else:
      num_total_ham+=1
      if predicted_cat=='ham':
        num_correct_ham+=1
    
  print(f"Correct Spam: {num_correct_spam}, Total Spam: {num_total_spam}")
  print(f"Accuracy Spam: {num_correct_spam/num_total_spam}")
  print(f"Correct Ham: {num_correct_ham}, Total Ham: {num_total_ham}")
  print(f"Accuracy Ham: {num_correct_ham/num_total_ham}")

if __name__ == '__main__':
    model, test_data = build_model()

    if not test_data:
        with open('test_data.json', 'r') as f:
            test_data = json.load(f)

    if test_data:
        test_model(model, test_data)
