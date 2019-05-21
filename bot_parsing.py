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
    date = date.replace(' ', '').replace('-', '.')
    # Beware of negative dates
    if date[0] == '.':
        date = '-' + date[1:]
    event = '*' + toLink(date)
    if place:
        event += ' / ' + toLink(place)
    return event + '. ' + descr + '. ' + toExtLink(link)


def add_biography(content, author, works, name, link, title):
    # Biographical information (birth and death)
    dob = author.get('birthdate', '')
    dod = author.get('deathdate', '')

    if dob or dod:
        pob = None
        pod = None

        if works:
            for a in works.get('@graph'):
                cand_pob = a.get('rdagroup2elements:placeOfBirth')
                cand_pod = a.get('rdagroup2elements:placeOfDeath')
                if cand_pob:
                    pob = cand_pob.split(' (')[0].split(',')[0]
                if cand_pod:
                    pod = cand_pod.split(' (')[0].split(',')[0]
                if pob or pod:
                    break

        birth = create_event(dob, pob, toLink('Naissance') + ' de ' + toLink(title + '|' + name), link)
        death = create_event(dod, pod, toLink('Décès') + ' de ' + toLink(title + '|' + name), link)

        if birth:
            content.append(birth)
        if death:
            content.append(death)


def get_work(works, work, content, name, surname, push, title_name):
    w_url = work.get('url')
    if w_url:
        w = get_json(w_url[0:-1] + '.json')[0]
        if not w:
            return
        label = sanitize(w.get('label'))
        label = (label[:150] + '...') if len(label) > 153 else label
        title = label + ' (' + surname + ')'
        event = toLink(key_word) + ' par ' + toLink(title_name + '|' + name) + ' de ' + toLink(title + '|' + label)
        info = get_json(w_url + 'rdf.jsonld')
        work_id = w.get('ark')[-9:]
        if info:
            for i in info.get('@graph'):
                cand_type = i.get('bnf-onto:subject')
                # Can somtimes be an array
                if cand_type and not isinstance(cand_type, str):
                    cand_type = cand_type[0]
                if cand_type:
                    event += ' (' + toLink(cand_type) + ')'
                    break
        work_line = create_event(w.get('publication'), None, event, w_url)
        if work_line:
            content.append(work_line)
        work_content = 'Wikidata: ([https://www.wikidata.org/wiki/Q386724 Q386724])\n\n'
        work_content += 'BnF ID: [' + w_url + ' ' + work_id[-9:] + ']\n\n'

        #Image
        image = w.get('image')
        if 'gallica.bnf.fr' in image:
            image += '.jpg'
            image_wo_ext = image.replace('.thumbnail.jpg','')
            work_content += '[' + image_wo_ext + ' ' + image + ']\n\n'

        work_content += work_line
        push_page(title, work_content, create_update)

def add_works(content, author, works, name, surname, push, title):
    if not works:
        return
    # Author's contributions
    allWorks = author.get('works', [])

    if allWorks:
        threads = []
        for work in allWorks:
            while len(threads) >= 10:
                threads = [t for t in threads if t.is_alive()]
            thread = Thread(target = get_work, args = (works, work, content, name, surname, push, title))
            thread.start()
            threads.append(thread)
        for t in threads:
            t.join()

    return len(allWorks)

def sanitize(s):
    if s:
        return s.strip().replace('[', '(').replace(']', ')')
    return s

def create_author_data(author_link, index, test, uuid_a=''):

    author = get_json(author_link + '.json')[0]

    if not author:
        return

    works  = get_json(author.get('url') + 'rdf.jsonld')

    # Define identity variables
    if 'surname' not in author:
        return

    surname   = sanitize(author['surname'])
    name      = sanitize(author.get('label').split('(')[0])
    title     = name
    if test:
        title = 'Test ' + title

    if uuid_a:
        title = title + ' (' + uuid_a + ')'

    content = []
    push = True
    if not uuid_a:
        push = import_page(content, title)
    add_biography(content, author, works, name, author_link, title)
    nb_works = add_works(content, author, works, name, surname, push, title)
    # Remove duplicates if bot already there
    content = list(set(content))
    content.sort()
    # This takes shorter years into account (999 vs 1001)
    content.sort(key=lambda x: int((x.split('[[')[1]).split(']]')[0].split('.')[0]))

    # Sort negative content differently
    neg_content = [x for x in content if '*[[-' in x]
    if neg_content:
        content = [c for c in content if c not in neg_content]
        neg_content.sort(reverse=True, key=lambda x: int((x.split('[[-')[1]).split(']]')[0].split('.')[0]))
        neg_content.extend(content)
        content = neg_content
        

    content.insert(0, 'Wikidata: ([https://www.wikidata.org/wiki/Q5 Q5])\n')
    content.insert(1, 'BnF ID: [' + author_link + ' ' + author_link[-9:] + ']\n')
    #Image
    image = author.get('image')
    if 'gallica.bnf.fr' in image:
        image += '.jpg'
        image_wo_ext = image.replace('.thumbnail.jpg','')
        content.insert(2, '[' + image_wo_ext + ' ' + image + ']\n')

    content_string = '\n'.join(content)

    if push:
        push_page(title, content_string, create_update)
        print('%06d: %s\n\t- %d works\n' % (index, title, nb_works), end='')
    else:
        f = open('log/exists_' + uuid.uuid4().hex[0:7] + '_' + title.replace(' ', '_') + '.log', 'w')
        f.write(content_string)
        f.close()
        print('%06d: %s \n\t##  EXISTS  ##\n\t- %d works\n' % (index, title, nb_works), end='')

