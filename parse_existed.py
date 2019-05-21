from bot_parsing import create_author_data
import sys
import os
import web_tools

def remove_extension(link):
    link = link.replace('.json', '')
    link = link.replace('/rdf.jsonld', '')
    return link

web_tools.Login.passw = str(sys.argv[1])

path = './log/Exists/'

files = []
uuids = []

for r, d, f in os.walk(path):
    for file in f:
        if '.log' in file:
            files.append(os.path.join(r, file))
            uuids.append(os.path.basename(file).split('_')[1])

index = 0


for file, u in zip(files[15:], uuids[15:]):
    f = open(file, 'r')
    for i, line in enumerate(f):
        if i == 2:
            link = line.split('[')[1].split(' ')[0]
    f.close()
    if 'ark:' in link:
        create_author_data(link, index, False, u)
    index += 1
