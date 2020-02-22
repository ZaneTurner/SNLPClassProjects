import nltk
from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords
import string

class DataPreprocessor:

    @staticmethod
    def clean_row(row, convert_to_lower=False):
        row = DataPreprocessor.remove_puncuation(row)
        if convert_to_lower:
            row = row.lower()
        #row = DataPreprocessor.remove_stop_words_from_single_row(row)
        #row = data_preprocessor.stem_words(row)
        row = row.replace('\n', '')
        return ['<s>'] + row.split() + ['</s>']

    @staticmethod
    def remove_stop_words_from_single_row(row):
        stop_words = set(stopwords.words('english'))
        word_tokens = nltk.word_tokenize(row)
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words and w.lower() not in stop_words:
                filtered_sentence.append(w)
        return filtered_sentence

    @staticmethod
    def stem_words(row):
        stemmed_row = ''
        lancaster = LancasterStemmer()
        for word in row:
            word = word.strip()
            stemmed_word = lancaster.stem(word)
            stemmed_row += stemmed_word + ' '
        return stemmed_row

    @staticmethod
    def remove_puncuation(row):
        return row.translate(str.maketrans('', '', string.punctuation))