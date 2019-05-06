from web_tools import get_json
from pathlib import Path
import sys

folder = "data/"

sparql_link_name = folder + "authors_link.txt"
author_list_name = folder + "authors.txt"
author_list_path = Path(author_list_name)

def list_author_links():
    '''
    Returns the list of the links to all authors listed in Gallica.
    Creates a file containing them all if not already created.
    '''
    author_links = []

    # Create the list of links to all authors.
    if not author_list_path.is_file():
        print('Dowloading JSON result from SPARQL request saved in ' + sparql_link_name)
        f = open(sparql_link_name, 'r')
        link = f.read()
        authors_json = get_json(link)['results']['bindings']
        authors_file = open(author_list_name, 'w')

        print('Parsing JSON result and saving it to ' + author_list_name)
        for author_json in authors_json:
            author = author_json['auteur']['value']
            print(author, file=authors_file)

    # Read file if already created.
    if not author_links:
        print('Reading links from ' + author_list_name +' file')
        authors_file = open(author_list_name, 'r')

        for author in authors_file:
            author_links.append(author.strip())

    print('Done')
    print()

    return author_links


