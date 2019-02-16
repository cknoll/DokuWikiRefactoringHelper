"""
This script takes two input files:

1. a list of all doku-wiki files
2. a list of namespace mappings , e.g. info/orga -> doc/org

It generates a list with entries for each file to rename/move
 `info/orga/concept.txt -> doc/org/concept.txt`

This file is aimed to be the input data for a script which actually performs the rename
"""


import os
from collections import defaultdict

from ipydex import IPS, activate_ips_on_exception
activate_ips_on_exception()


filelistpath = "../data/allfiles.txt"
nsmappath = "../data/nsmap.txt"
resfilepath = "../data/final_rename_list.txt"


with open(filelistpath) as txtfile:
    filelist = txtfile.readlines()

with open(nsmappath) as txtfile:
    nsmap = txtfile.readlines()


def path_to_tuple(pathstr):
    """
    Convert "aaa/bbb/xxx/yyy.zz" to ("aaa", "bbb", "xxx", "yyy.zz")
    :param pathstr:
    :return:
    """
    return tuple(os.path.normcase(pathstr).split(os.sep))

# find all atomic namespaces

ns_dict = defaultdict(list)

for path in filelist:
    path = path.strip()
    parts = path_to_tuple(path)
    if len(parts) == 1:
        ns_dict[("<toplevel_ns>",)].append(parts[-1])
    else:
        ns_dict[parts[:-1]].append(parts[-1])

# ↑
# keys are the existing namespaces
# values are the files belonging to them

# process mappings:
# ## 1st: explicit cases

ns_old_new_map = {}
for mapping in nsmap:
    mapping = mapping.strip()

    old, new = mapping.split(" -> ")

    old = path_to_tuple(old)
    new = path_to_tuple(new)
    ns_old_new_map[old] = new

# ## 2nd implicit cases (where subnamespaces have not been expliticly noted)
# example aaa -> xxx implies aaa/bbb -> xx/bbb if not noted explicitly

for old_ns_tuple in ns_dict.keys():
    if old_ns_tuple in ns_old_new_map:
        continue
    L = len(old_ns_tuple)
    for i in range(L):
        k = i + 1
        head = old_ns_tuple[:-k]
        tail = old_ns_tuple[-k:]
        new = ns_old_new_map.get(head)
        if new is not None:
            ns_old_new_map[old_ns_tuple] = new + tail
            print("implicit: ", old_ns_tuple, "->", new, tail)

            break

        # ensure that we terminated with a match
        assert new is not None

# list of 2-tuples of paths
final_map = []
final_str_list = []
for ns, filelist in ns_dict.items():
    new_ns = ns_old_new_map[ns]

    for file in filelist:
        path_old = os.sep.join(ns + (file,))
        path_new = os.sep.join(new_ns + (file,))
        final_map.append((path_old, path_new))

        tmp = "{:<80s} -> {}\n".format(path_old, path_new)
        final_str_list.append(tmp)


with open(resfilepath, "w") as txtfile:
    txtfile.writelines(final_str_list)


IPS()


