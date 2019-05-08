from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import requests
import json
import lxml.etree
import uuid


baseurl = 'http://wikipast.epfl.ch'

class Login:
    user = 'GallicaSPARQLBot'
    passw = None

class Edit:
    token = None
    cookie = None

def login_bot():

    if Edit.token and Edit.cookie:
        return Edit.token, Edit.cookie

    user    = Login.user
    passw   = Login.passw
    # Login request
    payload={'action':'query','format':'json','utf8':'','meta':'tokens','type':'login'}
    r1=requests.post(baseurl + '/wikipast/api.php', data=payload)

    #login confirm
    login_token=r1.json()['query']['tokens']['logintoken']
    payload={'action':'login','format':'json','utf8':'','lgname':user,'lgpassword':passw,'lgtoken':login_token}
    r2=requests.post(baseurl + '/wikipast/api.php', data=payload, cookies=r1.cookies)

    #get edit token2
    params3='?format=json&action=query&meta=tokens&continue='
    r3=requests.get(baseurl + '/wikipast/api.php' + params3, cookies=r2.cookies)
    edit_token=r3.json()['query']['tokens']['csrftoken']

    edit_cookie=r2.cookies.copy()
    edit_cookie.update(r3.cookies)

    Edit.token = edit_token
    Edit.cookie = edit_cookie

    return edit_token, edit_cookie


def import_page(content, title):
    params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"timestamp|user|comment|content" }
    params["titles"] = "API|%s" % quote(title.replace(' ', '_'))
    qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
    url = baseurl + '/wikipast/api.php?%s' % qs
    tree = lxml.etree.parse(urlopen(url))
    revs = tree.xpath('//rev')
    if revs and revs[-1].text:
        old_content = revs[-1].text.split('\n')
        listed_old_content = []
        no_list = True
        first_list = True
        for x in old_content:
            if x and x[0] == '*' and first_list:
                no_list = False
                listed_old_content.append(x)
            if x and x[0] != '*' and not no_list:
                first_list = False
        content.extend(listed_old_content)
        return False
    return True

def push_page(page, content, summary):
    name = page
    edit_token, edit_cookie = login_bot()
    payload = {'action':'edit','assert':'user','format':'json','utf8':'','text':content,'summary':summary,'title':name,'token':edit_token}
    r4 = requests.post(baseurl+'/wikipast/api.php',data=payload,cookies=edit_cookie)

def get_json(link):
    data = ['']
    try:
        with urlopen(link) as url:
            data = json.loads(url.read().decode())
    except Exception as e:
        f = open('log/fail_'+uuid.uuid4().hex[0:7] + '.log', 'w')
        f.write(link)
        f.close()
        print(link + ' could not be opened.')
        data = ['']
    return data

