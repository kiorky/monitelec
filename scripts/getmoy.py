#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import csv
import sys

from pprint import pprint

from collections import OrderedDict
from statistics import mean


fic = sys.argv[1]


class Cdialect(csv.excel):
    quoting = csv.QUOTE_ALL
    delimiter = ';'
    quotechar = '"'


computed = [
    'power',  # W/H
    'voltage',  # V
    'total',  # KW/H
    'current'  # A
]
EDF_KWH = 0.1579
nbdayspermonth = float(31)
nbhourspermonth = float(24 * nbdayspermonth)
nbminspermonth = float(60 * nbhourspermonth)
nbsecspermonth = float(60 * nbminspermonth)

with open(fic) as f:
    rows = [a for a in csv.DictReader(f, dialect=Cdialect)]
    for row in rows:
        for v in computed:
            try:
                row[v] = float(row[v])
            except ValueError:
                pass
        # try:
        #     # instance measure is in W/H
        #     # so we tranform the value back to W/S
        #     # to know how we consumed during this second of measure
        #     row['avgpwr'] = float(row['power']/(60.0*60.0))
        #     row['avgpwr'] = float(row['power']/(60.0*60.0))
        # except ValueError:
        #         pass
    nbsecmesured = float(len(rows))
    ratio = float(len(rows))/nbsecspermonth
    totals = OrderedDict()
    # for v in ['avgpwr'] + computed:
    for v in computed:
        avgk = 'avg_{}'.format(v)
        sumk = 'sum_{}'.format(v)
        totals[avgk] = mean(a[v] for a in rows)
        totals[sumk] = sum(a[v] for a in rows)
    #
    # reasoning is as the following :
    # we sum all of the measures and we have a instant measure for the
    # sum of time during all those seconds: with 4 measures, we have 4 seconds.
    # we then do a cross multiplication to get this measure for a month as an
    # avg and we transform back this value from W/S, to W/H then KW/h
    #
    # sumpwr | x(sumpwrmonth)
    # -------+---------------
    # nbsecs | nbsecspermonth
    #
    nbsecs = float(len(rows))
    ratio = nbsecs/nbsecspermonth
    sumpwrmonth = ((totals['sum_power']/nbsecs) * nbsecspermonth)/3600
    pprint(totals)
    print(
        'secs of measure (in sec, min, h, d: {},  {},  {},  {}'.format(
            nbsecs,
            round(nbsecs/60.0, 2),
            round(nbsecs/(60.0*60), 2),
            round(nbsecs/(60.0*60*24), 2)
        )
    )
    tt = round(sumpwrmonth/(1000), 2)
    print(
        'avgmonth pwr W/h, kW/h: {},  {}'.format(
            round(sumpwrmonth, 2),
            tt,
        )
    )
    print('EDF (€): {}'.format(round(EDF_KWH * tt, 2)))
# vim:set et sts=4 ts=4 tw=80:
