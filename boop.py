import argparse
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
import json 
import time

try:
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
except FileNotFoundError:
    print("config.json not found, creating file")
    data = {}
    data['boop'] = {}
    data['boop']['ip'] = "127.0.0.1"
    data['boop']['port'] = '9001'
    data['boop']['OSC'] = 'Misc/Boop'
    with open('config.json', 'w') as outfile:
        json.dump(data, outfile)
    print("config.json created, please edit and restart tool")
    time.sleep(5)
    exit()

boopsToday = 0  
boopsTotal = 0
file_name = 'boops.txt'
def read_first_line_as_int(file_name):
    try:
        with open(file_name, 'r') as file:
            first_line = file.readline().strip()
            if first_line:
                return int(first_line)
            else:
                return 0
    except FileNotFoundError:
        with open(file_name, 'w') as file:
            file.write('0')
        return 0
    
def sendOSCMessage(message):
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
    client.send_message("/chatbox/input", [message, True, False])

def boopreceiver(unused_addr, args):
    global boopsToday  # Declare that you're using the global variable
    global boopsTotal
    print("Boop received: ", args)
    if args == True:
        boopsToday += 1
        boopsTotal += 1
        with open(file_name, 'w') as file:
            file.write(str(boopsTotal))
        sendOSCMessage("Boop! \v Boops today: " + str(boopsToday) + "\v Boops Total: " + str(boopsTotal))  # Convert boopsToday to a string

boopsTotal = read_first_line_as_int(file_name)
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/avatar/parameters/" + data['boop']['OSC'] , boopreceiver)
server = osc_server.ThreadingOSCUDPServer((data['boop']['ip'], int(data['boop']['port'])), dispatcher)
server.serve_forever()

    