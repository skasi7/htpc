Installing osmc
===============

1. Install a fresh build into an SD (cofigure the network to fixed address).
2. Set max_usb_current=1 inside config.txt to be able to connect a USB drive.
3. Update to Kodi Krypton like this: https://discourse.osmc.tv/t/testing-kodi-17-krypton-builds-for-raspberry-pi-continued/14628
4. Install flexget like this: https://flexget.com/InstallWizard/Linux
5. Install cron (for flexget to run).
6. Schedule flexget like this: https://flexget.com/InstallWizard/Linux/Scheduling
7. Install deluged and deluge-console.
8. Schedule deluged like this (but changin user/group to osmc): http://dev.deluge-torrent.org/wiki/UserGuide/Service/systemd
8. Install the config.txt, Kodi, flexget and deluge config backups.
