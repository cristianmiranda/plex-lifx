import logging
import re
import socket
import urllib2
import xml.etree.ElementTree as ET

'''
    This is a helper class to provide assistance with all Plex API calls
'''
class Plex(object):

    def __init__(self, cfg):

        self.logger = logging.getLogger(__name__)
        self.cfg = cfg


    '''
        Get Media metadata from Plex users playing sessions.
        
        @param user_id  : Plex user id

        @return         : Media metadata
    '''
    def get_media_metadata_from_sessions(self, user_id):

        url = '{url}/status/sessions?X-Plex-Token={plex_token}'.format(url=self.cfg.get('plex-lifx',
          'mediaserver_url'), plex_token=self.cfg.get('plex-lifx','plex_token'))
        #self.logger.info('Fetching sessions status from {url}'.format(url=url))
    
        try:
            metadata = urllib2.urlopen(url, timeout=2)
        except urllib2.URLError, e:
            self.logger.error('urllib2 error reading from {url} \'{error}\''.format(url=url, error=e))
            return None
        except socket.timeout, e:
            self.logger.error('Timeout reading from {url} \'{error}\''.format(url=url, error=e))
            return None

        tree = ET.fromstring(metadata.read())
        videos = tree.findall('Video')

        if videos is None:
            self.logger.error('No videos found in sessions status feed.')
        else:
            for video in videos:
                m_id = video.get('key')
                user = video.find('User')
                if user.get('id') != user_id:
                    self.logger.info('Ignoring played item library-id={m_id}, because it is from another user.'
                        .format(m_id=m_id))
                    continue

                media_type = video.get('type')
                if video.get('type') != media_type:
                    self.logger.info('Ignoring played item library-id={m_id}, because it is not a ' + media_type + '.'
                        .format(m_id=m_id))
                    return None

                transcode = video.find('TranscodeSession')
                if transcode is None:
                    self.logger.info('Ignoring played item library-id={m_id}, could not determine transcoding information.'
                        .format(m_id=m_id))
                    return None

                player = video.find('Player')
                if player is None:
                    self.logger.info('Ignoring played item library-id={m_id}, could not determine player information.'
                        .format(m_id=m_id))
                    return None

                guid = video.get('guid')
                regex_str = 'com.plexapp.agents.thetvdb://([0-9]+)/([0-9]+)/([0-9]+).*'
                if media_type == 'movie':
                    regex_str = 'com.plexapp.agents.imdb://([a-zA-Z0-9]+).*'
                regex = re.compile(regex_str)
                m = regex.match(guid)              

                if m:
                    played_time = video.get('viewOffset')
                    duration = transcode.get('duration')
                    state = player.get('state')
                    progress = long(float(played_time)) * 100 / long(float(duration))

                    if media_type == 'movie':
                        return {
                            'imdb_id': m.group(1),
                            'movie_name': video.get('title'),
                            'duration': duration,
                            'progress': progress,
                            'srobbling' : state
                        }
                    else:
                        return {
                            'show_id': m.group(1),
                            'show_name': video.get('grandparentTitle'),
                            'season_number': m.group(2),
                            'episode_number': m.group(3),
                            'duration': duration,
                            'progress': progress,
                            'srobbling' : state
                        }
                else:
                    return None
        
        return None
