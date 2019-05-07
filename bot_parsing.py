from web_tools import *
from threading import Thread

key_word = 'Création'
create_update = 'GallicaSPARQLbot update'

def toExtLink(s):
    return '[' + s + ']'

def toLink(s):
    return toExtLink(toExtLink(s))

def create_event(date, place, descr, link):
    if not date:
        return ''
    date = date.replace('-', '.')
    event = '*' + toLink(date)
    if place:
        event += ' / ' + toLink(place)
    return event + '. ' + descr + '. ' + toExtLink(link)


def add_biography(content, author, works, name, link):
    # Biographical information (birth and death)
    dob = author.get('birthdate', '')
    dod = author.get('deathdate', '')

    if dob or dod:
        pob = None
        pod = None

        for a in works['@graph']:
            cand_pob = a.get('rdagroup2elements:placeOfBirth')
            cand_pod = a.get('rdagroup2elements:placeOfDeath')
            if cand_pob:
                pob = cand_pob.split(' (')[0]
            if cand_pod:
                pod = cand_pod.split(' (')[0]
            if pob or pod:
                break

        birth = create_event(dob, pob, toLink('Naissance') + ' de ' + toLink(name), link)
        death = create_event(dod, pod, toLink('Décès') + ' de ' + toLink(name), link)

        if birth:
            content.append(birth)
        if death:
            content.append(death)


def get_work(works, work, content, name, surname, push):
    w_url = work.get('url')
    if w_url:
        w = get_json(w_url[0:-1] + '.json')[0]
        if not w:
            print("Invalid work link given: " + w_url)
            return
        title = w.get('label') + ' (' + surname + ')'
        event = toLink(key_word) + ' par ' + toLink(name) + ' de ' + toLink(title + '|' + w.get('label'))
        info = get_json(w_url + 'rdf.jsonld')
        work_id = w.get('ark')[-9:]
        if info:
            for i in info['@graph']:
                cand_type = i.get('bnf-onto:subject')
                if cand_type:
                    event += ' (' + toLink(cand_type) + ')'
                    break
        work_line = create_event(w.get('publication'), None, event, w_url)
        if work_line:
            content.append(work_line)
        if push:
            work_content = 'Wikidata: ([https://www.wikidata.org/wiki/Q386724 Q386724])\n\n'
            work_content += 'BnF ID: [' + w_url + ' ' + work_id[-9:] + ']\n\n'
            work_content += work_line
            push_page(title, work_content, create_update)

def add_works(content, author, works, name, surname, push):
    # Author's contributions
    allWorks = author.get('works', [])

    if allWorks:
        threads = []
        for work in allWorks:
            while len(threads) >= 10:
                threads[0].join()
                del threads[0]
            thread = Thread(target = get_work, args = (works, work, content, name, surname, push))
            thread.start()
            threads.append(thread)
        for t in threads:
            t.join()

    return len(allWorks)

def sanitize(s):
    return s.strip().replace('É', 'E')

def create_author_data(author_link, index, test):

    author = get_json(author_link + '.json')[0]

    if not author:
        return

    works  = get_json(author.get('url') + 'rdf.jsonld')

    # Define identity variables
    firstname = sanitize(author.get('firstname'))
    surname   = sanitize(author.get('surname'))
    name      = surname
    if firstname:
        name = firstname + ' ' + name
    title = name
    if test:
        title = 'Test ' + title

    content = []
    push = import_page(content, title)
    add_biography(content, author, works, name, author_link)
    nb_works = add_works(content, author, works, name, surname, push)
    # Remove duplicates if bot already there
    content = list(set(content))
    content.sort()
    content.insert(0, 'Wikidata: ([https://www.wikidata.org/wiki/Q5 Q5])\n')
    content.insert(1, 'BnF ID: [' + author_link + ' ' + author_link[-9:] + ']\n')
    content_string = '\n'.join(content)

    if push:
        push_page(title, content_string, create_update)
        print('%06d: %s\n- %d works' % (index, name, nb_works))
    else:
        f = open('log/exists_'+uuid.uuid4().hex, 'w')
        f.write(content_string)
        f.close()

