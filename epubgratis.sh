#!/bin/sh

curl --silent $1 | grep "magnet:?" | cut -d\" -f 2 | python -c "import HTMLParser, sys; print HTMLParser.HTMLParser().unescape(sys.stdin.read())" | xargs -i deluge-console add "{}"
