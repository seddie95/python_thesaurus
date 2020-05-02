from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.error import HTTPError
from spellchecker import SpellChecker
import argparse
import sys


# set up parser parameters
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


def find_synonym(argv=None):
    """ Function to find synonyms for a string"""
    if argv is None:
        argv = sys.argv

    try:
        parser = create_parser()
        args = parser.parse_args(argv[1:])

        #  If word not spelled correctly get best guess of correct spelling
        correct_spelling = spell_check(args.string)

        # Remove whitespace before and after word and use underscore between words
        stripped_string = correct_spelling.strip()
        fixed_string = stripped_string.replace(" ", "_")
        print(f"{stripped_string}:")

        # Set the url using the amended string
        my_url = f'https://thesaurus.plus/thesaurus/{fixed_string}'
        # Open and read the HTML
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
        if len(argv) > 2:
            print("Phrase not found! Please try a different phrase.")

        else:
            print("Word not found! Please try a different word.")


if __name__ == "__main__":
    find_synonym(sys.argv)
