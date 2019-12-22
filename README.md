# DEPRECATED

sonosServer
===========

Server providing REST API to command Sonos components.

This little server provides a REST API on port 5000. It takes the queries and transform them into the corresponding SOAP queries, which are finally sent to the desired Sonos component.

The following queries are possible:
* ./ircode/<ircode>
* ./chose/<zonename>
* ./discover/<zonename>
* ./volUp
* ./volDown
* ./stop
* ./playpause
* ./rawcode/<IRcode>


This tool is very basic and completely designed for my requirements, which are:
* IR remote control with its receiver on an Arduino ethernet board
* Arduino (and other components in the network) consumes the REST API
* REST API must be converted into the Sonos SOAP calls
