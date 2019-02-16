"""

"""

import requests
from bs4 import BeautifulSoup
import dokuwiki

# noinspection PyUnresolvedReferences
from ipydex import IPS, activate_ips_on_exception
from conf import resfilepath, wikiurl, wikipage_fs, user_name, user_pw

activate_ips_on_exception()



# add a old pages as test


s = requests.Session()

dw = dokuwiki.DokuWiki(wikiurl, user_name, user_pw)


def get_main_form(url):

    res = s.get(url)
    bs = BeautifulSoup(res.text, 'html.parser')
    ff = bs.find_all("form")

    for f in ff:
        if f.get("id") == "dw__editform":
            return f

    raise ValueError("Main form not found at url: " + url)


def gen_edit_payload(form, content, summary="created"):

    inputs = form.find_all("input")
    payload = {}
    for inp in inputs:
        payload.update({inp.attrs["name"]: inp.attrs["value"]})

    payload.update({"wikitext": content, "summary": summary})

    assert form.attrs["method"] == "post"

    return payload


with open(resfilepath) as txtfile:
    filelist = txtfile.readlines()

for path1 in filelist:
    path2 = path1.replace("/", ":")
    # url = "{}{}&do=edit".format(wikiurl, wikipage_fs.format(path2))
    # form = get_main_form(url)

    # payload = gen_edit_payload(form, "12345")
    break



IPS()


