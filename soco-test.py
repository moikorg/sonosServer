

import soco


speakers = soco.discover()
if speakers == None:
    print ("Error, couldn't find any speaker")
    exit()


# Display a list of speakers
for speaker in speakers:
    print ("%s (%s)" % (speaker.player_name, speaker.ip_address))