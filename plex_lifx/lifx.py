import json
import logging
import os
import socket
import requests
import urlparse


class Lifx(object):

    def __init__(self, cfg):

        self.logger = logging.getLogger(__name__)
        self.cfg = cfg

    '''
        Common API methods
    '''    

    def get_token(self):

        return self.cfg.get('plex-lifx', 'lifx_token')


    def _do_lifx_auth_put(self, url, data):
        
        try:
            token = self.get_token()

            headers = {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token,
            }

            # timeout in seconds
            timeout = 5
            socket.setdefaulttimeout(timeout)

            if data:
                response = requests.put(url, data=data, headers=headers)
            else:
                response = requests.get(url, headers=headers)
            
            self.logger.info('Response: {0}'.format(response))
            return response
        except requests.HTTPError as e:
            self.logger.error('Unable to submit post data {url} - {error}'.format(url=url, error=e.reason))
            raise


    def _do_lifx_auth_get(self, url):
        
        return self._do_lifx_auth_put(url, None)

    '''
        LIFX API methods
    '''

    def set_state(self, light_id, power, color, brightness, duration):

        self.logger.info('Setting State to light {light_id} - Power: {power} - Color: {color} - Brightness: {brightness} - Duration: {duration}.'
            .format(light_id=light_id, power=power, color=color, brightness=brightness, duration=duration))

        url = 'https://api.lifx.com/v1/lights/id:' + light_id + '/state'
        data = {}

        if power:
            data['power'] = power

        if color:
            data['color'] = color

        if brightness:
            data['brightness'] = brightness

        if duration:
            data['duration'] = duration        
        
        json_data = json.dumps(data)

        try:
            return self._do_lifx_auth_put(url, json_data)
        except:
            return None
