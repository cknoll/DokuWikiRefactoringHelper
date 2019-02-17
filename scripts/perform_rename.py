"""

"""

import pickle
import dokuwiki
import time
from selenium import webdriver
import selenium.common.exceptions as se

# noinspection PyUnresolvedReferences
from ipydex import IPS, activate_ips_on_exception
from conf import resfilepath, wikiurl, wikipage_fs, user_name, user_pw, cookiedumppath


activate_ips_on_exception()


def add_old_pages_for_testing():

    L = len(file_map_list)
    for i, path1 in enumerate(file_map_list):
        path1 = path1.split(" -> ")[0].strip()
        path2 = path1.replace("/", ":").replace(".txt", "")

        dw.pages.set(path2, "1234567")
        print("{}/{}".format(i, L))


def delete_all_pages():

    ll = dw.pages.list()

    for l in ll:
        dw.pages.delete(l["id"])


def perform_login():

    driver.get(wikiurl)
    li = driver.find_element_by_link_text("Log In")
    li.click()

    username = driver.find_element_by_name("u")
    password = driver.find_element_by_name("p")

    username.send_keys(user_name)
    password.send_keys(user_pw)

    btns = driver.find_elements_by_tag_name("button")
    for b in btns:
        if b.text.lower() == "log in":
            submit_button = b
            break
    else:
        raise ValueError("Submit Button not found")

    submit_button.click()

    pickle.dump(driver.get_cookies(), open(cookiedumppath, "wb"))


def load_login_cookies():
    # does not work:
    # Component returned failure code: 0x80070057 (NS_ERROR_ILLEGAL_VALUE)
    cookies = pickle.load(open(cookiedumppath, "rb"))
    for cookie in cookies[1:]:
        driver.add_cookie(cookie)


def rename_page(idx, depth=0):

    if depth > 10:
        # this happens if also iterated attempts to perform the rename do not
        # succeed
        raise ValueError("something went wrong with the move plugin")

    name_old, name_new = file_map_list[idx].split(" -> ")
    name_old = name_old.strip().replace("/", ":").replace(".txt", "")
    name_new = name_new.strip().replace("/", ":").replace(".txt", "")

    content_old = dw.pages.get(name_old)
    url = "{}{}".format(wikiurl, wikipage_fs.format(name_old))

    if content_old == "":
        print("did not exist: ", url)
        return

    content_new = dw.pages.get(name_new)
    if content_new is not "":
        print("page was already renamed", url, "->", name_new)
        return

    driver.get(url)

    btn = driver.find_element_by_class_name("plugin_move_page")
    btn.click()

    time.sleep(0.5)
    fields = driver.find_elements_by_name("id")
    for f in fields[::-1]:
        if not f.get_attribute("type") == "text":
            continue
        try:
            f.clear()
            f.send_keys(name_new)

            break
        except se.ElementNotInteractableException as ex:
            pass
    else:
        print("Error on page", url, ". Try again:", depth)
        return rename_page(idx, depth=depth+1)
        # raise ValueError("Could not find valid field to introduce the new name")

    btns = driver.find_elements_by_tag_name("button")

    for b in btns:
        if b.text.lower() == "rename":
            b.click()
            break
    else:
        raise ValueError("Could not find rename button")

    redirect_content = "This Page was moved to [[{}]] in a different namespace.".format(name_new)

    dw.pages.set(name_old, redirect_content)

    print("old url: ", url)


with open(resfilepath) as txtfile:
    file_map_list = txtfile.readlines()

dw = dokuwiki.DokuWiki(wikiurl, user_name, user_pw)

if 0:
    delete_all_pages()
    add_old_pages_for_testing()

driver = webdriver.Firefox()
perform_login()

for idx in range(len(file_map_list)):
    rename_page(idx)


# IPS()



