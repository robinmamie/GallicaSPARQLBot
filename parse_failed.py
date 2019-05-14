from bot_parsing import create_author_data
import sys
import os
import web_tools

def remove_extension(link):
    link = link.replace('/rdf.jsonld', '')
    link = link.replace('.json', '')
    return link

web_tools.Login.passw = str(sys.argv[1])

path = './log/Fail/'

files = []
for r, d, f in os.walk(path):
    for file in f:
        if '.log' in file:
            files.append(os.path.join(r, file))

index = 0

for file in files:
    f = open(file, 'r')
    link = f.read()
    f.close()
    link = remove_extension(link)
    if 'ark:' not in link:
        create_author_data(link, index, False)
    index += 1

