import logging
import os
import re
import time

from plex import Plex
from lifx import Lifx


dimmed = False
playing = False

# Target User ID (will be gone when multiuser gets supported)

USER_ID = '1'


'''
    Keeps an eye on Plex Media Server sessions status
'''
def monitor(config):
    
    global dimmed
    global playing

    logger = logging.getLogger(__name__)
    
    while True:
        time.sleep(1)

        plex = Plex(config)
        metadata = plex.get_media_metadata_from_sessions(USER_ID)

        if metadata:
            
            playing = True
            lifx = Lifx(config)
            light_id = config.get('plex-lifx', 'lifx_light_id')
            state = metadata['srobbling']

            if state == 'playing' and not dimmed:
                
                logger.info("PLAYING - Dimming till 0 light bulb {light_id}".format(light_id=light_id))
                lifx.set_state(light_id, 'on', None, 0.5, None)
                time.sleep(1)
                lifx.set_state(light_id, 'off', None, 0, None)
                dimmed = True

            elif state != 'playing' and dimmed:
                
                logger.info("PAUSED - Dimming till 0.5 light bulb {light_id}".format(light_id=light_id))
                lifx.set_state(light_id, 'on', None, 0.5, None)
                dimmed = False

        elif playing:
            
            logger.info("STOPPED - Turning light bulb {light_id} on".format(light_id=light_id))
            lifx.set_state(light_id, 'on', None, 1, None)
            dimmed = False
            playing = False
