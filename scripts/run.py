#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
import time
import csv
import pyHS100
from pyHS100 import SmartPlug


class Cdialect(csv.excel):
    quoting = csv.QUOTE_ALL
    delimiter = ';'
    quotechar = '"'


def write(rows, mode='w', *a, **kw):
    if not isinstance(rows, list):
        rows = [rows]
    with open(output, mode) as csvfile:
        writer = csv.DictWriter(csvfile, titles, dialect=Cdialect)
        for row in rows:
            writer.writerow(row)


output = os.environ.get('OUTPUT', '/data/out/out.csv')
doutput = os.path.dirname(output)
host = os.environ.get('PLUG', 'plug')
titles = ['date', 'power', 'voltage', 'current', 'total']
rtitles = dict([(a, a) for a in titles])

if not os.path.exists(doutput):
    os.makedirs(doutput)

try:
    content = open(output).read(1024)
except Exception:
    content = ''

if not content:
    write(rtitles)

print('Hit control C to stop scanning')
while True:
    now = datetime.datetime.now()
    try:
        sd = SmartPlug(host)
        state = sd.get_emeter_realtime()
    except pyHS100.smartdevice.SmartDeviceException:
        continue
    state["date"] = now.strftime('%Y-%m-%d %H:%M:%S')
    write(state, mode='a')
    time.sleep(1)
# vim:set et sts=4 ts=4 tw=120:
