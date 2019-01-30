#!/usr/bin/env python3
import curses
import datetime
import signal
import sys
import time

import jenkins
from tabulate import tabulate

import cursesTui

# https://python-jenkins.readthedocs.io/en/latest/api.html

serverURL = "http://cv.jenkins.couchbase.com/"

# user = server.get_whoami()
# print(user['fullName'])

# jobs = server.get_jobs()
# for i in jobs:
#     print(i['name'])

# Curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()

server = jenkins.Jenkins(serverURL)
version = server.get_version()


def poll_queue(status):
    fileOut = []
    queue_info = server.get_queue_info()
    fileOut.append(str(status) + " " + time.strftime("%H:%M:%S") + " " + str(status))
    fileOut.append("Current Queue length: " + str(len(queue_info)))
    buildTable = []
    for i in queue_info:
        colour = None
        for text in (i['task']['color']).split('_'):
            if text in ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']:
                colour = str(text)
        commit = ""
        change_no = ""
        owner = ""
        for j in i.get('actions'):
            try:
                for x in j.get('parameters'):
                    if x.get('name') == 'GERRIT_CHANGE_SUBJECT':
                        commit = str(x.get('value'))
                    elif x.get('name') == 'GERRIT_CHANGE_NUMBER':
                        change_no = str(x.get('value'))
                    elif x.get("name") == 'GERRIT_CHANGE_OWNER_NAME':
                        owner = str(x.get('value'))
            except TypeError:
                continue
        buildID = str(i['id'])
        taskName = str(i['task']['name'])
        buildWhy = str(i['why'])
        dateTime = (datetime.datetime.now() - datetime.datetime.fromtimestamp(i['inQueueSince'] / 1e3))
        timeInQueue = str(dateTime).split('.')[0]
        buildTable.append([buildID, taskName, change_no, commit, owner, buildWhy, timeInQueue])

        # outputStr = (buildID + ",\t" + taskName + ",\t" + buildWhy + ",\tChange no: " + change_no + ",\tCommit: " + commit)
        # print(colored(outputStr, colour))

    headers = ['BuildID', 'Job Name', 'Gerrit Change No', 'Commit Header', 'Owner', 'Queue Reason', 'Time in queue']
    # fileOut.append(tabulate(buildTable, headers=headers))
    for n in tabulate(buildTable, headers=headers).split('\n'):
        fileOut.append(n)
    return fileOut



def sigterm_handler(signal, frame):
    print('Hasta la vista')
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    sys.exit(0)


signal.signal(signal.SIGTERM, sigterm_handler)
status = ['|', '/', '-', '\\']
refreshBase = time.time()
refreshTime = 15
try:
    screen = cursesTui.Screen(poll_queue('x'))
    while True:
        for st in status:
            try:
                screen.input_stream_no_loop(2)
            except curses.error as error:
                print("Curses Error, try widening the console area")
                raise error
            # time.sleep(1)
            if time.time() - refreshBase > refreshTime:
                screen.update_items(poll_queue(st))
                refreshBase = time.time()


except KeyboardInterrupt:
    print('Cheerio')
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    sys.exit(0)
