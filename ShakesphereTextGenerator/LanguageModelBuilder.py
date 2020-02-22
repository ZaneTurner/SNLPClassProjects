'''
Zane Turner
Statistical Natural Language Processing

this program constructs a sentence that is something similar to what Shakespheare himself would have said.
It uses old Shakespheare plays text in order work properly. It can easily be modified to generate other
sentences using any corpus of data.

'''

from DataPreprocessor import DataPreprocessor as preprocessor
import math
import random


class LanguageModelBuilder:

    @classmethod
    def build_text(cls, sample_text_file, starting_words):

        cleaned_rows = cls.clean_file(sample_text_file)
        bigrams = cls.calculate_all_bigrams(cleaned_rows)
        unigrams = cls.get_unigram_counts(cleaned_rows)

        normalized_bigrams = cls.calculate_normalized_bigrams(unigrams, bigrams)
        normalized_bigrams = sorted(normalized_bigrams.items(), key=lambda x: -x[1])
        normalized_bigrams_words = [k for k,v in normalized_bigrams]

        next_word_dictionary = cls.convert_to_next_word_dictionary(normalized_bigrams_words)
        print(cls.get_shannons_next_word(next_word_dictionary, starting_words))

    @staticmethod
    def clean_file(file_name):
        cleaned_rows = []
        with open(file_name) as file:
            for line in file.readlines():
                cleaned_rows.append(preprocessor.clean_row(line, True))
        return cleaned_rows

    @staticmethod
    def calculate_all_bigrams(clean_rows):
        bigrams = {}
        for row in clean_rows:
            for word_index in range(len(row)-1):

                bigrams[(row[word_index],row[word_index+1])] = bigrams.get((row[word_index],row[word_index+1]), 0) + 1
        return bigrams

    @staticmethod
    def get_unigram_counts(clean_rows):
        unigrams = {}
        for row in clean_rows:
            for word in row:
                unigrams[word] = unigrams.get(word, 0)+1
        return unigrams

    @staticmethod
    def calculate_normalized_bigrams(unigrams, bigrams):
        normalized_bigrams = {}
        for (word_1, word_2), count in bigrams.items():
            normalized_bigrams[(word_1, word_2)] = count/unigrams.get(word_1)
        return normalized_bigrams

    @staticmethod
    def calculate_probability_of_a_given_sentence_occurring(sentence, normalized_bigrams, number_of_tokens):
        sentence = preprocessor.clean_row(sentence, True) # make it into the same format that I built my model on
        probability = 0
        for i in range(len(sentence)-1):
            probability += math.log10(normalized_bigrams.get((sentence[i],sentence[i+1]),1/number_of_tokens))
        return probability

    @staticmethod
    # make it random
    def get_shannons_next_word(sorted_normalized_bigrams, inital_bigram):
        sentence = preprocessor.clean_row(inital_bigram)
        sentence = sentence[1:len(sentence)-1]
        seen = set()
        for i in range(8):
            if sentence[-1] not in sorted_normalized_bigrams:
                sentence.append('<s>')
            possible_next_words = sorted_normalized_bigrams.get(sentence[-1])
            possible_next_words = possible_next_words[:5]
            next_word = random.choice(possible_next_words)
            seen.add(next_word)
            sentence.append(next_word)
        return sentence

    @staticmethod
    def convert_to_next_word_dictionary(normalized_words):
        next_word_dictionary = {}
        for w1,w2 in normalized_words:
            if w2 == '</s>':
                continue
            next_word_dictionary[w1] = next_word_dictionary.get(w1, []) + [w2]
        return next_word_dictionary


language_model_builder = LanguageModelBuilder()
language_model_builder.build_text('ShakespeareDocuments.txt', 'the women')

