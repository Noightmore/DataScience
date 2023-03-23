import factorize
import queen
import censor_number
import text_analysis
import get_words
import sifrovani


def main():
    my_factors = factorize.prime_factorization(100)
    print(my_factors)

    queen.print_queen_board(16, 16, 5, 4)

    censor_number.censor_number(5, 10)

    analysis = text_analysis.analyze_text_file('book.txt')
    #print(analysis[1])

    wanted_words = get_words.get_top_words_by_count(analysis[1], 10, 5)
    print(wanted_words)

    zasifrovana_zprava = sifrovani.encrypt('Hello world!', 5)
    print(zasifrovana_zprava)
    rozsifrovana_zprava = sifrovani.decrypt(zasifrovana_zprava, 5)
    print(rozsifrovana_zprava)


if __name__ == '__main__':
    main()


