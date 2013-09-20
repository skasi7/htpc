Instructions to install revised newpct plugin
=============================================

- Apply the patch with the command:
  > patch urlrewrite_newpct.py < urlrewrite_newpct.patch

  urlrewrite_newpct.py file can be found at:
    /usr/local/lib/python2.7/dist-packages/flexget/plugins/urlrewrite_newpct.py
    (This is the debian path for Python 2.7, find yours).

Instructions to install malformed HTML in formlogin patch
=========================================================

- Apply the patch with the command:
  > patch plugin_formlogin.py < plugin_formlogin.py.patch

  plugin_formlogin.py file can be found at:
    /usr/local/lib/python2.7/dist-packages/flexget/plugins/plugin_formlogin.py
    (This is the debian path for Python 2.7, find yours).

Instructions to install listdir encoding patch
==============================================

- Apply the listdir patch with the command:
  > patch listdir.py < listdir.py.patch

  listdir.py file can be found at:
    /usr/local/lib/python2.7/dist-packages/flexget/plugins/input
    (This is the debian path for Python 2.7, find yours).

Instructions to install newpct plugin for flexget (added in r3248)
==================================================================

- Copy the urlrewrite_newpct.py file to:
  /usr/local/lib/python2.7/dist-packages/flexget/plugins/
  (This is the debian instalation path for Python 2.7, find the appropiate for
  your distribution)

- Check the right plugin installation with the command:
  > flexget --plugins

- Apply the qualities patch with the command:
  > patch qualities.py < qualities.py.patch

  qualities.py file can be found at:
    /usr/local/lib/python2.7/dist-packages/flexget/utils
    (Again, this is the debian path for Python 2.7, find yours).

- Change your configuration (config.yml) to use the installed plugin. A simple
  example can be found within this directory.)
