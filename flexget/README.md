Instructions to install revised newpct plugin
=============================================
Due to the recent www.newpct.com ISP block, www.newpct1.com site has been enabled. Update your urlrewrite plugin in Flexget to be able to download again.

- Copy the new plugin to:
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

