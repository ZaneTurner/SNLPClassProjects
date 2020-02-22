import sys
import csv
from DataPreprocessor import DataPreprocessor


class BigramFinder:

    @classmethod
    def print_bigrams_ranked_by_frequency_then_chi_squared_table(cls, n, reviews_file, output_file):

        most_frequent_bigrams = cls.get_most_frequent_bigrams(n, reviews_file)
        most_significant_according_to_chi_squared = cls.get_most_signicant_chi_squared_bigrams(n, reviews_file)

        with open(output_file, 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['frequency bigram results', 'chi-squared bigram results'])
            for frequent_bigram, significant_bigram in zip(reversed(most_frequent_bigrams), reversed(most_significant_according_to_chi_squared)):
                writer.writerow([frequent_bigram[0], significant_bigram[0]])

    @classmethod
    def get_most_frequent_bigrams(cls, n, reviews_file):
        bigrams = cls._count_bigrams_by_frequency(reviews_file)
        return sorted(bigrams.items(), key=lambda x: x[1])[-n:]

    @classmethod
    def get_most_signicant_chi_squared_bigrams(cls, n, reviews_file):
        bigrams = cls._count_bigrams_by_frequency(reviews_file)
        first_word_bigram_occurrences, second_word_bigram_occurrences = cls._calculate_first_and_second_word_bigram_occurrences(bigrams)
        bigrams_chi_squared = cls._count_bi_grams_using_chi_squared(bigrams, first_word_bigram_occurrences, second_word_bigram_occurrences)
        return sorted(bigrams_chi_squared.items(), key=lambda x:x[1])[-n:]

    @staticmethod
    def _count_bigrams_by_frequency(file_name):
        with open(file_name, 'r', encoding='mac-roman', newline='\r\n') as file:
            bigrams = {}
            unigrams = {}
            data_preprocessor = DataPreprocessor()
            for row in file.readlines():
                row = data_preprocessor.clean_row(row)
                for index in range(len(row)-1):
                    unigrams[row[index]] = unigrams.get(row[index])
                    bigrams[(row[index], row[index+1])] = bigrams.get((row[index], row[index+1]),0)+1
            return bigrams

    @classmethod
    def _count_bi_grams_using_chi_squared(cls, bigrams_by_frequency, first_word_bigram_occurrences,second_word_bigram_occurrences):
        # i could make this class much cleaner before I turn this in
        bigrams_chi_squared = {}
        for k, observed_value in bigrams_by_frequency.items():  # bigrams by frequency
            w1 = k[0]
            w2 = k[1]

            w2_count_2 = second_word_bigram_occurrences.get(w2)
            w1_count_1 = first_word_bigram_occurrences.get(w1)

            chi_square_1_1 = observed_value
            chi_square_1_2 = w2_count_2 - observed_value
            chi_square_2_1 = w1_count_1 - observed_value
            chi_square_2_2 = len(bigrams_by_frequency) - chi_square_1_1 - chi_square_1_2 - chi_square_2_1
            sum_across_top = chi_square_1_1 + chi_square_2_1
            sum_across_bottom = chi_square_1_2 + chi_square_2_2
            sum_down_left = chi_square_1_1 + chi_square_1_2
            sum_down_right = chi_square_2_1 + chi_square_2_2

            chi_square_value = cls._calculate_square(sum_across_top, sum_down_left, len(bigrams_by_frequency), chi_square_1_1)
            chi_square_value += cls._calculate_square(sum_across_top, sum_down_right, len(bigrams_by_frequency), chi_square_2_1)
            chi_square_value += cls._calculate_square(sum_across_bottom, sum_down_left, len(bigrams_by_frequency), chi_square_1_2)
            chi_square_value += cls._calculate_square(sum_across_bottom, sum_down_right, len(bigrams_by_frequency), chi_square_2_2)

            bigrams_chi_squared[k] = chi_square_value
        return bigrams_chi_squared

    @staticmethod
    def _calculate_square(v1, v2, v3, observed):
        expected_value = v1 * (v2/v3)
        return ((observed - expected_value)**2)/expected_value


    @staticmethod
    def _calculate_first_and_second_word_bigram_occurrences(bigrams):
        first_word_bigram_occurrences = {}
        second_word_bigram_occurrences = {}
        for value in bigrams:
            first_word_bigram_occurrences[value[0]] = first_word_bigram_occurrences.get(value[0], 0) + 1
            second_word_bigram_occurrences[value[1]] = second_word_bigram_occurrences.get(value[1], 0) + 1
        return first_word_bigram_occurrences, second_word_bigram_occurrences


if __name__=="__main__":
    bigram_finder = BigramFinder()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    bigram_finder.print_bigrams_ranked_by_frequency_then_chi_squared_table(100,input_file,output_file)