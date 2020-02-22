import nltk
from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords


class DataPreprocessor:

    @staticmethod
    def clean_row(row):
        row = DataPreprocessor.remove_puncuation(row)
        row = DataPreprocessor.remove_stop_words_from_single_row(row)
        #row = data_preprocessor.stem_words(row)
        return row

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