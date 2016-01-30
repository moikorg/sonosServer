__author__ = 'mike'

#from soco import discover
import soco

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
    """ looks for the Zone with the given name (argument) """
    for zones in soco.discover():
        if zones.player_name == room_name:
            return zones


def play_favorite_station(zone,station2play):
    """ play the station within the favorite radio stations """
    stations = zone.get_favorite_radio_stations()
    for fave in stations['favorites']:
        if fave['title'].find(station2play) > -1:
            uri = fave['uri']
            # TODO seems at least & needs to be escaped - should move this to play_uri and maybe escape other chars.
            uri = uri.replace('&', '&amp;')
            metadata = meta_template.format(title=fave['title'], service=tunein_service)
            zone.play_uri( uri, metadata)
            break
