# fin_ninja_asic2

Sample code to control the LTE SIM with onbox-python

## Use Case Description

Describe the problem this code addresses, how your code solves the problem, challenges you had to overcome as part of the solution, and optional ideas you have in mind that could further extend your solution.
- When EEM detects a FTP session start, it launches python script and the script changes the SIM contract speed from slow mode to fast mode.
- If the SIM contract change is successful, sends a success message to the administrator by Webexteams.
- If it fails, sends a log file by Webexteams.
- When EEM detects a FTP session close, it re-launches python script and the script changes the SIM contract speed from fast mode to slow mode.
- If it fails, sends a log file by Webexteams.
              
## Installation

1. Need a SORACOM SIM subscription to use this script.
2. Copy "sim_control.py" to flash on your LTE router.
3. Kick this script via EEM on IOS-XE. Please refer the example-eem.txt.

## Configuration

You have to set some env valiables for sending messsages to webex teams.
 - WEBEXTOKEN : set your webex teams bot token.
 - ROOMID     : set your Room ID in webex teams.
 
## Usage

usage: SIM Speed conftrol for SORACOM API [-h] [-L] [-s] [-S SPEED]
                                          [-H HOSTNAME]

optional arguments:
  -h, --help            show this help message and exit
  -L, --log             Get status log: Send logs to webex teams for troubleshoot.
  -s, --status          Get SIM Status: Get current sim speed from SORACOM center.
  -S SPEED, --speed SPEED
                        Set SIM Status <fast | slow>
  -H HOSTNAME, --hostname HOSTNAME
                        Router name


### DevNet Sandbox

NA

## Known issues

NA

## Getting help

If you have questions, concerns, bug reports, etc., please create an issue against this repository.

## Author(s)

This project was written and is maintained by the following individuals:

* Team Financial Ninja: <hsakabe@cisco.com>, <kikuta@cisco.com>, <knagao@cisco.com>, <knakashi@cisco.com>
