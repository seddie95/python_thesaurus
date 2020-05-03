from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.error import HTTPError
from spellchecker import SpellChecker
import argparse


def create_parser():
    """Function to parse the user entered arguments"""
    parser = argparse.ArgumentParser(description='find synonyms for a word or phrase')
    parser.add_argument('string', type=str, help='Enter word or words', nargs='*')
    return parser


def spell_check(string):
    """Function to correct the spelling of a string"""
    # instantiate spellchecker
    spell = SpellChecker()
    misspelled = spell.unknown(string)

    # Iterate over the words and replace the misspelled words
    for index, word in enumerate(string):
        if word in misspelled:
            string[index] = spell.correction(word)

    # Join the strings together
    corrected_string = ' '.join(string)
    return corrected_string


def find_synonym():
    """ Function to find synonyms for a string"""

    word_count = 0
    # Take in arguments from command line
    try:
        parser = create_parser()
        args = parser.parse_args()

        # If word not spelled correctly get best guess of correct spelling
        correct_spelling = spell_check(args.string)

        # update word count
        word_count = len(correct_spelling)

        # Remove whitespace before and after word and use underscore between words
        stripped_string = correct_spelling.strip()
        fixed_string = stripped_string.replace(" ", "_")
        print(f"{stripped_string}:")

        # Set the url using the amended string
        my_url = f'https://thesaurus.plus/thesaurus/{fixed_string}'
        # Open and read the HTMLz
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()

        # Parse the html into text
        page_soup = soup(page_html, "html.parser")
        word_boxes = page_soup.find("ul", {"class": "list paper"})
        results = word_boxes.find_all("div", "list_item")

        # Iterate over results and print
        for result in results:
            print(result.text)

    except HTTPError:
        if word_count > 1:
            print("Phrase not found! Please try a different phrase.")

        else:
            print("Word not found! Please try a different word.")


if __name__ == "__main__":
    find_synonym()
