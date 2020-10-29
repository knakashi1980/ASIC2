# -*- coding: utf-8 -*-
import pycurl
import cli
import os
import json
from ciscosparkapi import CiscoSparkAPI
from argparse import ArgumentParser
from StringIO import StringIO
from datetime import datetime

def get_sim_status():

    url = 'metadata.soracom.io/v1/subscriber'
    buffer = StringIO()

    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json', 'Accept: aapplication/json'])
    curl.setopt(pycurl.CUSTOMREQUEST, 'GET')
    curl.setopt(pycurl.CONNECTTIMEOUT, 5)
    curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
    curl.perform()
    json_data = json.loads(buffer.getvalue())
    print(json_data['speedClass'])

def set_sim_speed(sim_speed):

    url = 'metadata.soracom.io/v1/subscriber/update_speed_class'
    buffer = StringIO()

    if sim_speed == "fast":
        speed = '{"speedClass":"s1.fast"}'
    elif sim_speed == "slow":
        speed = '{"speedClass":"s1.slow"}'
    else:
        print("Invalid argument")
        return 0

    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json', 'Accept: aapplication/json'])
    curl.setopt(pycurl.CUSTOMREQUEST, 'POST')
    curl.setopt(pycurl.POSTFIELDS, speed)
    curl.setopt(pycurl.CONNECTTIMEOUT, 5)
    curl.setopt(pycurl.WRITEFUNCTION, buffer.write)

    try:
        curl.perform()
    except pycurl.error as e:
        print(e)
        return 0
    else:
        json_data = json.loads(buffer.getvalue())
        print(json_data['speedClass'])
        return 1

    return 0

def teamsbot(*args):

    bot_token = os.environ['WEBEXTOKEN']
    room_id = os.environ['ROOMID']

    try:
        api = CiscoSparkAPI(access_token=bot_token)
    except:
        print("Can't connect to webex teams")

    if len(args) == 1:
        message = args[0]
        try:
            api.messages.create(roomId=room_id, markdown=message)
        except:
            print("Can't create a new message")
    elif len(args) == 2:
        message = args[0]
        filename = args[1]
        try:
            api.messages.create(roomId=room_id, markdown=message, files=[filename])
        except:
            print("Can't create a new meeage with file")
    else:
        print("Invalid args")
        return

def get_logs():

    command_list_file = '/flash/command_list'
    logfile_raw = '/flash/logfile_' + datetime.now().strftime('%Y-%m-%d-%H%M%S')
    logfile_name = logfile_raw + "tar.gz"

    try:
        fd = open(command_list_file, "r")
    except OSError as e:
        print(e)
    else:
        result = fd.read()
        fd.close()

    try:
       fd = open(logfile_raw, 'w')
    except OSError as e:
       print(e)
    else:
        for line in result.split('\n'):
            msg = '### ' + datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ' - ' + line +  ' ###'
            fd.write(msg)
            fd.write(cli.cli(line))
        fd.close()

    cmd = 'tar zcvf ' + logfile_name + " " + logfile_raw
    os.system(cmd)

    cmd = "rm -f " + logfile_raw
    os.system(cmd)

    return(logfile_name)

# main function
if __name__ == "__main__":

    parser = ArgumentParser("SIM Speed conftrol for SORACOM API")
    parser.add_argument("-L", "--log", action='store_true', help="Get status log", required=False)
    parser.add_argument("-s", "--status", action='store_true', help="Get SIM Status", required=False)
    parser.add_argument("-S", "--speed", help="Set SIM Status <fast | slow>", required=False)
    parser.add_argument("-H", "--hostname", help="Router name", required=False)

    # parse argumetns
    args = parser.parse_args()
    router_name = args.hostname
    sim_speed = args.speed
    sim_status = args.status
    log_status = args.log

    if log_status == True:
        logfile_name = get_logs()
        msg = "Get Log file from " + router_name
        teamsbot(msg, logfile_name)
    elif sim_status == True:
        get_sim_status()
        msg = "Get SIM Status: " + router_name
        teamsbot(msg)
    elif sim_speed != None:
        if set_sim_speed(sim_speed) != 0:
            msg = router_name + ':' + " Set SIM Speed to " + sim_speed
            teamsbot(msg)
        else:
            print("failed\n")
