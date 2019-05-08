from bot_parsing import create_author_data
from list_authors import list_author_links
from threading import Thread
import sys
import time
import web_tools

if len(sys.argv) != 2:
    print('Please give the password of GallicaSPARQLBot')
    sys.exit(2)

web_tools.Login.passw = str(sys.argv[1])

START      = 3000
NB_THREADS = 20
NUM        = 7000

links = list_author_links()
nb_authors = len(links)
testMode = False

#create_author_data('http://data.bnf.fr/ark:/12148/cb11885942z', 0, False)

print('There are ' + str(nb_authors) + ' to parse in total. Test mode is ' + str(testMode) + '.')
print('The bot will parse authors number ' + str(START) + ' to ' + str(START + NUM - 1) + '.')
wish = input('Do you wish to proceed? (Y/n) ')
if wish != '' and wish != 'y' and wish != 'Y':
    sys.exit()

start_time = time.time()
threads = []
for i in range(START, START+NUM):
    while len(threads) > NB_THREADS:
        threads = [t for t in threads if t.is_alive()]
    t = Thread(target=create_author_data, args=(links[i], i, testMode))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
total_time = round(time.time() - start_time)

print()
print("### %d authors created in %s minutes %s seconds ###" % (NUM, round(total_time / 60), total_time % 60))
