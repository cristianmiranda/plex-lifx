Plex LIFX
==========

**plex-lifx** dims your LIFX light bulb when Plex starts playing. It'll set brightness to 50% when paused and restores original bright when stopped.

See it in action: https://youtu.be/S_Jn5HDuxLU

A few points:

* plex-lifx is an out of process tool. Meaning it is not a Plex Media Server plug-in. This tool runs separately of your Plex Media Server.
Must be run on the Plex Media Server
* Uses python standard library. Python is the only requirement to run this application

Installation
----

###Linux, OSX

Fetch and install the source from the github repo.

```
git clone https://github.com/cristianmiranda/plex-lifx.git
cd plex-lifx
python setup.py install
```

Alternatively, you can fetch the latest zip from github.

```
wget https://github.com/cristianmiranda/plex-lifx/archive/master.zip
unzip master.zip
cd plex-lifx-master
python setup.py install
```

You're done :smile:

Configuration
-----------

The plex-lifx configuration file (plex_lifx.conf) is installed to ~/.config/plex-lifx/ . The following configuration values are available.

If you're running Plex Media Server on a Linux based operating system, things should work out of the box.

```
[plex-lifx]
# REQUIRED: mediaserver_url is the location of the http service exposed by Plex Media Server. The default values should be 'ok', assuming you're running the plex scrobble script from the same server as your plex media server
mediaserver_url = http://localhost:32400

# REQUIRED: Where do you wish to write the plex-lifx log file.
log_file = /tmp/plex_lifx.log

# REQUIRED: LIFX Personal API token
lifx_token = cb3d4e8f6494e59q09911a63b42ff836df623ad16fd633f101123456789025b5

# REQUIRED: LIFX Light ID
lifx_light_id = f47321245611

# REQUIRED: required only when using authentication even in local networks
# See how to get your token @ https://support.plex.tv/hc/en-us/articles/204059436-Finding-your-account-token-X-Plex-Token
plex_token=E1vy91cJ24yop3iJPq
```

Running
--------

```
$ python plex-lifx.py
```

You may wish to leave the service running in the background. On a POSIX system, wrap the script in the no-hangup utility.

```
$ nohup python plex-lifx.py &
```

Troubleshooting
-------------

For tailing the logs:
```
tail -f /tmp/plex_lifx.log
```

Browse the github issues list to review old bugs or log a new problem.  See https://github.com/cristianmiranda/plex-lifx/issues?q=


Contributing
-----------

Please log an issue or a pull request with any fixes.

Thanks
------

Inspired on https://github.com/bstascavage/plexHue
