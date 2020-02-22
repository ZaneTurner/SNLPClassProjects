'''
Zane Turner
11/25/2019
'''
from sklearn.feature_extraction.text import CountVectorizer
import csv
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import time
import os
import psutil

word_dictionary = {}

def get_vocab_size(corpus):
    total_vocab = set()
    for row in corpus:
        total_vocab = total_vocab.union(set(row.split(' ')), total_vocab)
    return len(total_vocab)


def convert_csv_column_into_document(training_file_location, column, convert_to_binary=False):
    corpus = []
    with open(training_file_location, encoding='mac-roman') as csv_file:
        file = csv.reader(csv_file)
        prev = None
        for i,row in enumerate(file):
            if i != 0:
                if convert_to_binary:
                    if prev != row[1]:
                        corpus.append(1) if float(row[column]) >= 0 else corpus.append(0)
                else:
                    for word in row[column].split():
                        if word not in word_dictionary:
                            word_dictionary[word] = len(word_dictionary)+1
                    if prev != row[1]:
                        corpus.append(row[column])
                    else:
                        corpus[-1] += row[column]
            prev = row[1]
    return corpus

def convert_document_into_bag_of_words(document, max_features):
    cv = CountVectorizer(ngram_range=(1,1), max_features=max_features)
    bow = cv.fit_transform(document)
    return bow.toarray()

def convert_each_word_into_number(document):
    resulting_document = []
    for row in document:
        result = []
        for word in row.split():
            result.append(word_dictionary.get(word, 0))
        resulting_document.append(list(result)) # maybe cast as list? that would be so dumb
    return resulting_document

def calculate_metrics(actual, predictions):
    print('accuracy: ' + str(accuracy_score(actual, predictions)))
    print('precision: ' + str(precision_score(actual, predictions)))
    print('recall: ' + str(recall_score(actual, predictions)))
    print('f1 score: ' + str(f1_score(actual, predictions)))

file_location = 'LSTMData.csv'
label_column = 12
preprocessed_data_column = 9
features_count = 1000


x_document = convert_csv_column_into_document(file_location, preprocessed_data_column, convert_to_binary=False)
y_document = convert_csv_column_into_document(file_location, label_column, convert_to_binary=True)
x_document = convert_document_into_bag_of_words(x_document, features_count)
x_train, x_test, y_train, y_test = train_test_split(x_document, y_document)

process = psutil.Process(os.getpid())
print('mem pre: ' + str(process.memory_info().rss))
start_time = time.time()
svc = SVC()
svc.fit(X=x_train, y=y_train)
predictions = svc.predict(x_test)
calculate_metrics(y_test, predictions)
print("--- %s seconds ---" % (time.time() - start_time))
print('svc memory')
print(process.memory_info().rss)

start_time = time.time()
nb = GaussianNB()
nb.fit(X=x_train, y=y_train)
predictions = nb.predict(x_test)
calculate_metrics(y_test, predictions)
print("--- %s seconds ---" % (time.time() - start_time))
print(process.memory_info().rss)

start_time = time.time()
rf = RandomForestClassifier()
rf.fit(X=x_train, y=y_train)
predictions = rf.predict(x_test)
calculate_metrics(y_test, predictions)
print("--- %s seconds ---" % (time.time() - start_time))
print(process.memory_info().rss)