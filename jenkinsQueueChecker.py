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
        if len(commit) > 100:
            commit = commit[:97] + "..."
        buildID = str(i['id'])
        taskName = str(i['task']['name'])
        buildWhy = str(i['why'])
        if len(buildWhy) > 75:
            buildWhy = buildWhy[:72] + "..."
        dateTime = (datetime.datetime.now() - datetime.datetime.fromtimestamp(i['inQueueSince'] / 1e3))
        timeInQueue = str(dateTime).split('.')[0]
        buildTable.append([buildID, taskName, change_no, commit, owner, buildWhy, timeInQueue])

    headers = ['BuildID', 'Job Name', 'Gerrit No.', 'Commit Header', 'Owner', 'Queue Reason', 'Queue Time']
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
statusIndex = 0
refreshBase = time.time()
refreshTime = 15
try:
    screen = cursesTui.Screen(poll_queue('x'))
    while True:
        try:
            screen.input_stream_no_loop(2)
        except curses.error as error:
            print("Curses Error, try widening the console area")
            raise error
        # time.sleep(1)
        if time.time() - refreshBase > refreshTime:
            screen.update_items(poll_queue(status[statusIndex]))
            statusIndex = (statusIndex + 1) % 4
            refreshBase = time.time()


except KeyboardInterrupt:
    print('Cheerio')
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    sys.exit(0)
