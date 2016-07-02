import os
from distutils.core import setup

NAME = 'plex-lifx'
VERSION = '1.0.0'

setup(
    name = 'plex_lifx',
    version = VERSION,
    author = 'Cristian Miranda',
    author_email = 'crism60@gmail.com',
    description = ('Plex playback dimming LIFX bulbs automatically'),
    license = 'MIT',
    url = 'https://github.com/cristianmiranda/plex-lifx',
    scripts = ['scripts/plex-lifx.py'],
    packages=['plex_lifx'],
    data_files = [(
      os.path.expanduser('~/.config/{0}'.format(NAME)),
      ['conf/plex_lifx.conf'],
      )]
)
