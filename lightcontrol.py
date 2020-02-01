import re
import socket
import struct
import sys
import os
from time import sleep
from mss import mss
from colorthief import ColorThief



def discoverBulbs():
    mcast_grp = ('239.255.255.250', 1982) #multicast address
    disco_msg = b"M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.259:1982\r\nMAN: \"ssdp:discover\"\r\nST: wifi_bulb" #multicast message

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((get_ip(), 6969)) #bind to local ip + selected port
    sock.settimeout(5)
    ttl = struct.pack('b', 1) #set ttl value so that we don't go outside the local network
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    
    expression = re.compile("yeelight://.................")
    
    data = None
    server = None
    
    try:
        sent = sock.sendto(disco_msg, mcast_grp)
        data, server = sock.recvfrom(1024)
        response = data.decode()
    except socket.timeout:
        print("Timed out")
    finally:
        sock.close()
        if data is None:
            return("No bulbs found")
        led_ip_match = expression.findall(response)

        led_ip = led_ip_match.pop()

        led_ip = led_ip.replace("yeelight://", "")
        split_ip = led_ip.split(":")

        final_ip = split_ip.pop(0)
        final_port = split_ip.pop()
        
        return(final_ip, final_port) 

def control(led_ip, led_port, r, g, b, time):
    color = (r * 65536) + (g * 256) + b
    msg = "{\"id\": 1, \"method\": \"set_rgb\", \"params\":[%d, \"smooth\", %d]}\r\n" % (color, time)
    
    bytes_msg = msg.encode()
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sock.connect((led_ip, led_port))
    sock.send(bytes_msg)
    #print(sock.recv(1024).decode())
    sock.close()

def get_ip(): #thanks stackoverflow, this is the only one that works the way I want it
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def ambient():
    with mss() as sct:
        filename = sct.shot(mon=-1, output='screen.png')
        color_thief = ColorThief('screen.png')
        dominant_color = color_thief.get_color(quality=1)
        palette = color_thief.get_palette(color_count=3)
        return(palette[1])



bulbs = discoverBulbs()


while True:
    accentColor = ambient()
    red = accentColor[0]
    green = accentColor[1]
    blue = accentColor[2]
    time = 10000
    control(bulbs[0].encode(), int(bulbs[1]), red, green, blue, time)
    os.remove("screen.png")
    print("Executing, sleeping for 10 min")
    sleep(600) #sleep for 10 min
    


#print(accentColor[0])
#print(accentColor[1])
#print(accentColor[2])

#red = int(input("Enter in a red value(0-255): "))
#green = int(input("Enter in a green value(0-255): "))
#blue = int(input("Enter in a blue value(0-255): "))
#time = int(input("Enter in the transition time(ms): "))



