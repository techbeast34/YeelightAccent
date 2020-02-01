# YeelightAccent
Takes accent color of all monitors and changes the color of Yeelight LED strip/RGB bulb to the 2nd dominant color of each screen. Loops every 5 minutes.

Uses python3

This should work on Linux/macOS/Windows

Make sure you enable LAN control for your fixture. I have not tested this with multiple Yeelight fixtures on the same network, so behavior may be unexpected with multiple fixtures. 

## External Dependencies
[mss](https://pypi.org/project/mss/), can be installed through `pip install mss`

[colorthief](https://pypi.org/project/colorthief/), can be installed through `pip install colorthief`

## Bugs/Weird Anomalies
It seems like colorthief hates blue in my experimentation, ex. If 2 of my 3 screens have a grey/black color and the last screen is dominantly blue, it will be purpleish, but if the same screen is dominantly green or red, it will match that color, more or less.
