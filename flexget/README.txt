Instructions to install newpct plugin for flexget
================================================

- Copy the urlrewrite_newpct.py file to:
  /usr/local/lib/python2.7/dist-packages/flexget/plugins/
  (This is the debian instalation path for Python 2.7, find the appropiate for
  your distribution)

- Check the right plugin installation with the command:
  > flexget --plugins

- Apply the qualities patch with the command:
  > patch qualities.py < qualities.py.patch

  qualities.py file can be found at:
    /usr/local/lib/python2.7/dist-package/flexget/utils
    (Again, this is the debian path for Python 2.7, find yours).

- Change your configuration (config.yml) to use the installed plugin. A simple
  example can be found within this directory.)
