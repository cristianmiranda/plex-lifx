#!/usr/bin/env python
import os
import sys
import platform
import logging
import time
import threading
import ConfigParser
from optparse import OptionParser

from plex_lifx.plex_monitor import monitor

def platform_log_directory():
    ''' Retrieves the default platform specific default log location.
        This is called if the user does not specify a log location in
        the configuration file.
    '''

    LOG_DEFAULTS = {
        'Darwin': os.path.expanduser('~/Library/Logs/Plex Media Server.log'),
        'Linux': '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs/Plex Media Server.log',
        'Windows': os.path.join(os.environ.get('LOCALAPPDATA', 'c:'), 'Plex Media Server/Logs/Plex Media Server.log'),
        'FreeBSD': '/usr/local/plexdata/Plex Media Server/Logs/Plex Media Server.log',
    }

    return LOG_DEFAULTS[platform.system()]


def main(config):
    ''' The main thread loop

    Args:
        config (ConfigParser obj) : user specific configuration params
    '''

    logger.info('Starting log monitor thread...')
    log_watch = threading.Thread(target=monitor, args=(config,))
    log_watch.start()

    # main thread ended/crashed. exit.
    log_watch.join()
    sys.exit(1)

if __name__ == '__main__':

    p = OptionParser()
    p.add_option('-c', '--config', action='store', dest='config_file',
        help='The location to the configuration file.')
    p.set_defaults(config_file=os.path.expanduser(
      '~/.config/plex-lifx/plex_lifx.conf'))
    (options, args) = p.parse_args()

    if not os.path.exists(options.config_file):
        print 'Exiting, unable to locate config file {0}. use -c to specify config target'.format(
            options.config_file)
        sys.exit(1)

    # apply defaults to *required* configuration values.
    config = ConfigParser.ConfigParser(defaults = {
        'config file location': options.config_file,
        'mediaserver_url': 'http://localhost:32400',
        'log_file': '/tmp/plex_lifx.log'
      })
    config.read(options.config_file)

    FORMAT = '%(asctime)-15s [%(process)d] [%(name)s %(funcName)s] [%(levelname)s] %(message)s'
    logging.basicConfig(filename=config.get('plex-lifx',
      'log_file'), format=FORMAT, level=logging.DEBUG)
    logger = logging.getLogger('main')

    # dump our configuration values to the logfile
    for key in config.items('plex-lifx'):
        logger.debug('config : {0} -> {1}'.format(key[0], key[1]))

    m = main(config)
