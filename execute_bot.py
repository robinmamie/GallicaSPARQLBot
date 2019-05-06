from bot_parsing import create_author_data
from list_authors import list_author_links
from threading import Thread
import sys
import time
import web_tools

# TODO remove when necessary
#create_author_data("https://data.bnf.fr/en/13893113/georges_delerue", test=True)
#create_author_data("https://data.bnf.fr/fr/13538475/claude_gillot", test=True)
#create_author_data("https://data.bnf.fr/fr/11916491/claude_monet", test=True)
#create_author_data("http://rts.ch", test=True)
if len(sys.argv) != 2:
    print('Please give the password of GallicaSPARQLBot')
    sys.exit(2)

web_tools.Login.passw = str(sys.argv[1])

START      = 0
NB_THREADS = 50
NUM        = 1

links = list_author_links()
nb_authors = len(links)
testMode = True
pushMode = True

#create_author_data('https://data.bnf.fr/ark:/12148/cb119297200', 0, True, True)

print('There are ' + str(nb_authors) + ' to parse. Test mode is ' + str(testMode) + '.')
wish = input('Do you wish to proceed? (Y/n) ')
if wish != '' and wish != 'y' and wish != 'Y':
    sys.exit()

start_time = time.time()
threads = []
for i in range(START, START+NUM):
    while len(threads) > NB_THREADS:
        threads[0].join()
        del threads[0]
    t = Thread(target=create_author_data, args=(links[i], i, testMode, pushMode))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
total_time = round(time.time() - start_time)

print()
print("### %d authors created in %s minutes %s seconds ###" % (NUM, round(total_time / 60), total_time % 60))
