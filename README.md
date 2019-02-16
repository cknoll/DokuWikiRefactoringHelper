# DokuWikiRefactoringHelper

This project aims to facilitate refactoring a dokuwiki.

## Tools:
* `rename_ns.py`
    * Generate a list of all old and new (sub)namespaces
    * Input: list of all dokuwiki files (full paths), list of explicit renames
* `rename_pages.py`
    * Perform the renaming using the plugin [move-plugin](https://www.dokuwiki.org/plugin:move)
    * also generate a redirect-page at the original url

