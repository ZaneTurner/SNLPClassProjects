import nltk
import re
import csv
from DataPreprocessor import DataPreprocessor

'''
;
Takes the following inputs -
1. A txt/csv file or simply a hardcoded set of sentences (input data)
2. A list of lists of phrases in the following format

[
['likely', 'like', 'likes']
['short-run', 'short run']
['day', 'days]
['animal', cat', 'dog', 'rhino', 'tiger']
]

then gives the following output

a csv file that contains counts of each words inside each list, and makes a row for it. 
For example,

        likely, short-run, day, animals
row1         1,         2,   3,       1
row2         2,         3,   10,      0
row3         5,         7,   4,       2

notes -
all punctuation is removed automatically by the code
if you want to name the columns yourself, you can send in a list containing the column names.
Additionally, if you want to rename the output file you can send it in as a parameter

I really could just build a NLP software, it wouldn't be bad to do
'''


class PhraseCounter:

    @classmethod
    def count_phrases(cls, input_file='', phrases=[[]], column_names=[], output_file='output_file.csv'):
        patterns = cls.build_regrex_patterns_for_each_phrase(phrases)
        csv_reader = csv.reader(open(input_file, 'r', encoding='mac-roman'))
        csv_writer = csv.writer(open(output_file, 'w', encoding='mac-roman'))
        cls.write_header_column(phrases, column_names, csv_writer)
        cls.write_counts_of_each_phrase(csv_reader, csv_writer, patterns)

    @staticmethod
    def write_counts_of_each_phrase(csv_reader, csv_writer, patterns):
        print(patterns)
        data_preprocessor = DataPreprocessor()
        for row in csv_reader:
            cleaned_row = data_preprocessor.remove_punctuation(''.join(row))
            resulting_row = []
            for pattern in patterns:
                number_of_occurrences = len(re.findall(pattern, cleaned_row))
                resulting_row.append(number_of_occurrences)
            csv_writer.writerow(resulting_row)

    @staticmethod
    def write_header_column(phrases, column_names, csv_writer):
        if not column_names:
            for phrase in phrases:
                column_names.append(phrase[0])
        csv_writer.writerow(column_names)

    @staticmethod
    def build_regrex_patterns_for_each_phrase(phrases):
        patterns = []
        for phrase in phrases:
            patterns.append('|'.join(phrase))
        return patterns


input_file = 'BobDylanLyrics.csv'
pc = PhraseCounter()
pc.count_phrases(input_file=input_file,
                 phrases=[['knock', 'knocking'],
                          ['long', 'extended', 'lengthy'],
                          ['eclipes', 'moon']],
                 column_names=['knocking', 'reference to long', 'moon related'])