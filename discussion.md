Aktuelle Version geht prinzipiell

auf der alten Seite ist dann nur ein Hinweis und ein Link.

Automatische Umleitung wäre besser.

Drei diskutierte wege:

### symbolische Links auf dem Server ⚡
- redirects kommen nicht im Browser an
- alte Namensräume geistern noch immer rum → verwirrung
-  → Wollen wir nicht ⚡

### Plugin http://www.dokuwiki.org/plugin:redirect
- ⊕ funktioniert lokal
- ⊖ wäre weitere dauer-dependency
- carsten dafür, sebi kann damit leben, jonas dagegen

### apache redirects
- ⊕ keine zusätzliche dauer-dependency
- ⊖ RewriteRules sind Bedingung dafür, dass redirects gehen.
    - Carsten: habe ich lokal nicht testen können weil auf rosetta bestimmte RewriteRules aktiv sind, die ich nicht lokal umgesetzt bekommen habe
- jonas dafür


⊕⊖




relevante Links:

https://www.dokuwiki.org/rewrite

http://localhost/dokuwiki-master/doku.php


## aus dem fsfw-ansible:

    # RewriteEngine on
    #       # insanity inspired from https://stackoverflow.com/a/1279758/1248008
    # RewriteCond %{QUERY_STRING} ^id=([^&:]*):([^&]*)((&.*)?)
    # RewriteRule ^(/doku\.php)$ $1?id=%1/%2%3 [N]
    # RewriteCond %{QUERY_STRING} ^id=([^&]*)((&(.*))?)
    # RewriteRule ^(/doku\.php)$ /doku.php/%1?%4 [R=301,L]
