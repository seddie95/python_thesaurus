from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.error import HTTPError
from spellchecker import SpellChecker
import sys


def spell_check(string):
    """Function to correct the spelling of a string"""
    # instantiate spellchecker
    spell = SpellChecker()

    # Split the word into a list and pass it to the spellchecker
    split_string = string.split()
    misspelled = spell.unknown(split_string)

    # Iterate over the words and replace the misspelled words
    for index, word in enumerate(split_string):
        if word in misspelled:
            split_string[index] = spell.correction(word)

    # Join the strings together
    string = ' '.join(split_string)
    return string


def find_synonym(argv):
    """ Function to find synonyms for a string"""
    #  If word not spelled correctly get best guess of correct spelling
    correct_spelling = spell_check(argv)

    # Remove whitespace before and after word and use underscore between words
    stripped_string = correct_spelling.strip()
    fixed_string = stripped_string.replace(" ", "_")
    print(f"{stripped_string}:")

    try:
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
        print("Page not found")


if __name__ == "__main__":
    find_synonym(' '.join(sys.argv[1:]))
