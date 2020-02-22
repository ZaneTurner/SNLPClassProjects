import re


class DataPreprocessor:

    @staticmethod
    def remove_punctuation(string):
        return re.sub('[^\w\s]','',string)

