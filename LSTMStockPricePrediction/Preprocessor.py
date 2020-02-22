import pandas as pd
from nltk.stem import PorterStemmer
import csv
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import sent_tokenize, word_tokenize, pos_tag

# saved file as default encoding and then in worked?
ps = PorterStemmer()

features_column_names=['Analyst', 'Words analyst said']
label_column_names=['vwretd']
stop_words = set(stopwords.words('english'))

# stem words and remove stop words
with open(r'E:\NLPpaper\analyst_information_dated.csv', 'w') as csvfile:
    with open(r'E:\NLPpaper\analyst_data_with_labels.txt') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count+=1
                continue
            #print(row)
            stemmed_words = []
            sentence = row[9].translate(str.maketrans('', '', string.punctuation))
            sentence = sentence.lower()
            sentence = sentence.split(" ")
            for word in sentence:
                if word == '-':
                    continue
                if word.isdigit():
                    continue
                if word == 'hi':
                    continue
                stemmed_words.append(ps.stem(word))
            filtered_sentence = [w for w in stemmed_words if not w in stop_words]
            filtered_sentence = list(filter(None, filtered_sentence))
            final_sentence = ' '.join(filtered_sentence)
            csvfile.write(final_sentence + '\n')


exit()

features_data_frame = pd.read_csv(r'E:\NLPpaper\analyst_data_with_labels.txt', usecols=features_column_names, encoding='mac_roman')
labels_data_frame = pd.read_csv(r'E:\NLPpaper\analyst_data_with_labels.txt', encoding='mac_roman', usecols=label_column_names)
print(labels_data_frame.head())
features_data_frame['stemmed_words'] = features_data_frame['Words analyst said'].apply(lambda x: [ps.stem(y) for y in x])
features_data_frame.to_csv(r'E:\NLPpaper\stemmed_data.csv')

# first lets just clean all the data


# should i create a big file with all the different analysts? Or
# just for each analyst create a specific domain and save all of those domains
# into memory?