#!/usr/bin/python

from flask import Flask

from soco import SoCo
from soco import discover

import syslog
import time
import re

import sonos_helper


app = Flask(__name__)

zone_wohnzimmer = sonos_helper.get_speaker("Wohnzimmer")
print zone_wohnzimmer.player_name
print zone_wohnzimmer.play_mode
print zone_wohnzimmer.ip_address
#print zone_wohnzimmer.volume
#print zone_wohnzimmer.get_current_track_info()
#print zone_wohnzimmer.get_current_transport_info()
#sonos_helper.adjust_volume(zone_wohnzimmer,10)
#sonos_helper.adjust_volume(zone_wohnzimmer,-15)

print "start web server"

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
    print "Got IR code %s, playing %s" % (code,station)
    sonos_helper.play_favorite_station(zone_wohnzimmer,station)
    zone_wohnzimmer.play()
    return ""


@app.route('/chose/<zonename>')
def chose(zonename):
    zone_wohnzimmer = sonos_helper.get_speaker(zonename)
    print "%s chosen..." % zonename
    return ""

@app.route('/discover/<zonename>')
def discover(zonename):
    return sonos_helper.get_speaker(zonename).ip_address


@app.route('/volUp/')
def volUp():
    if zone_wohnzimmer.volume < 30:
	factor = 4
    else:
	factor = 6
    sonos_helper.adjust_volume(zone_wohnzimmer,factor)
    return "Volume: %s" % zone_wohnzimmer.volume

@app.route('/volDown/')
def volDown():
    if zone_wohnzimmer.volume < 30:
	factor = -4
    else:
	factor = -6
    sonos_helper.adjust_volume(zone_wohnzimmer,factor)
    return "Volume: %s" % zone_wohnzimmer.volume

@app.route('/stop/')
def stop():
    zone_wohnzimmer.stop();
    return "Playing stoped"

@app.route('/playpause/')
def playpause():
    if (zone_wohnzimmer.get_current_transport_info()['current_transport_state'] == 'PLAYING'):
        zone_wohnzimmer.pause()
    elif (zone_wohnzimmer.get_current_transport_info()['current_transport_state'] == 'PAUSED_PLAYBACK'):
        zone_wohnzimmer.play()
    elif (zone_wohnzimmer.get_current_transport_info()['current_transport_state'] == 'STOPPED'):
        zone_wohnzimmer.play()
    return zone_wohnzimmer.get_current_transport_info()['current_transport_state']




if __name__ == '__main__':
    app.run(host='0.0.0.0')


# Documentation
# http://soco.readthedocs.org/en/latest/
