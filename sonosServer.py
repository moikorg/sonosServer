#!/usr/bin/env python3
import soco
from flask import Flask

# from soco import SoCo
# from soco import discover

# import syslog
# import time
# import re

import sonos_helper

meta_template = '<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/" xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/"><item id="R:0/0/0" parentID="R:0/0" restricted="true"><dc:title>{title}</dc:title><upnp:class>object.item.audioItem.audioBroadcast</upnp:class><desc id="cdudn" nameSpace="urn:schemas-rinconnetworks-com:metadata-1-0/">{service}</desc></item></DIDL-Lite>'
tunein_service = 'SA_RINCON65031_'


#####################################################
def adjust_volume(zone, factor):
    """ Adjust the volume up or down with a factor from 1 to 100 """

    volume = zone.volume
    if volume + factor > 100:
        zone.volume = 100
    elif volume + factor < 0:
        zone.volume = 0
    else:
        zone.volume = volume + factor


def get_speaker(room_name):
    """ looks for the Zone with the given name (room_name) """
    for zones in soco.discover():
        if zones.player_name == room_name:
            return zones


def play_favorite_station(zone, station2play):
    """ play the station within the favorite radio stations
        zone: describes which zone will be used
        station2play: is the information about the station that should be played
    """
    stations = zone.get_favorite_radio_stations()
    for fave in stations['favorites']:
        if fave['title'].find(station2play) > -1:
            uri = fave['uri']
            # TODO seems at least & needs to be escaped - should move this to play_uri and maybe escape other chars.
            uri = uri.replace('&', '&amp;')
            metadata = meta_template.format(title=fave['title'], service=tunein_service)
            zone.play_uri(uri, metadata)
            break


#######################################################################################################################

app = Flask(__name__)

zone_wohnzimmer = sonos_helper.get_speaker("Wohnzimmer")
print("Started for player: %s" % zone_wohnzimmer.player_name)
print("Play mode: %s" % zone_wohnzimmer.play_mode)
print("Player's IP: %s" % zone_wohnzimmer.ip_address)
# print(zone_wohnzimmer.volume)
# print(zone_wohnzimmer.get_current_track_info())
# print(zone_wohnzimmer.get_current_transport_info())
# sonos_helper.adjust_volume(zone_wohnzimmer,10)
# sonos_helper.adjust_volume(zone_wohnzimmer,-15)

print("start web server")


@app.route('/')
def hello_world():
    return 'Hello Worlddddd!'


@app.route('/ircode/<code>')
def ircode(code):
    if code == '1':
        station = "Freiburg"
    elif code == '2':
        station = "Fribourg"
    elif code == '3':
        station = "DRS 3"
    elif code == '4':
        station = "SWR3"
    elif code == '5':
        station = "The Point"
    elif code == '6':
        station = "The Office"
    elif code == '7':
        station = "The Rock"
    elif code == '8':
        station = "SwissGroove"
    elif code == '9':
        station = "Swiss Pop"
    else:
        station = "Freiburg"
    print("Got IR code %s, playing %s" % (code, station))
    sonos_helper.play_favorite_station(zone_wohnzimmer, station)
    zone_wohnzimmer.play()
    return ""


@app.route('/rawcode/<IRcode>')
def rawIDcode(IRcode):
    print("RawCode query: IRcode is %s" % IRcode)
    return ""


@app.route('/chose/<zonename>')
def chose(zonename):
    zone_wohnzimmer = sonos_helper.get_speaker(zonename)
    print("%s chosen..." % zonename)
    return ""


@app.route('/discover/<zonename>')
def discover(zonename):
    return sonos_helper.get_speaker(zonename).ip_address


@app.route('/volUp/')
def vol_up():
    if zone_wohnzimmer.volume < 30:
        factor = 4
    else:
        factor = 6
    sonos_helper.adjust_volume(zone_wohnzimmer, factor)
    return "Volume: %s" % zone_wohnzimmer.volume


@app.route('/volDown/')
def vol_down():
    if zone_wohnzimmer.volume < 30:
        factor = -4
    else:
        factor = -6
    sonos_helper.adjust_volume(zone_wohnzimmer, factor)
    return "Volume: %s" % zone_wohnzimmer.volume


@app.route('/stop/')
def stop():
    zone_wohnzimmer.stop()
    return "Playing stoped"


@app.route('/playpause/')
def play_pause():
    if zone_wohnzimmer.get_current_transport_info()['current_transport_state'] == 'PLAYING':
        zone_wohnzimmer.pause()
    elif zone_wohnzimmer.get_current_transport_info()['current_transport_state'] == 'PAUSED_PLAYBACK':
        zone_wohnzimmer.play()
    elif zone_wohnzimmer.get_current_transport_info()['current_transport_state'] == 'STOPPED':
        zone_wohnzimmer.play()
    return zone_wohnzimmer.get_current_transport_info()['current_transport_state']


if __name__ == '__main__':
    app.run(host='0.0.0.0')


# Documentation
# http://soco.readthedocs.org/en/latest/
