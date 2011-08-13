#!/usr/bin/env python
# encoding: utf-8
"""
rrule2text.py

Created by William Bert on 2011-08-12.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
from datetime import datetime

# TODO Add i18n

import dateutil
from dateutil.rrule import *
from dateutil.rrule import weekday
from dateutil.rrule import rrule as rr
#import dateutil.rrule.weekday as rrule_weekday
from dateutil.relativedelta import relativedelta as rd
#import dateutil.relativedelta.weekday as rd_weekday

from int2word import int2word

        
class Rrule2textError(ValueError):
    pass

class rrule2text(rr): # class rr is class rrule in module dateutil.rrule

    WEEKDAY_MAP = {
        u'SU': u"Sunday",
        u'MO': u"Monday",
        u'TU': u"Tuesday",
        u'WE': u"Wednesday",
        u'TR': u"Thursday",
        u'FR': u"Friday",
        u'SA': u"Saturday",
    }
    
    ORDINAL = (
        (1,  u'first'),
        (2,  u'second'),
        (3,  u'third'),
        (4,  u'fourth'),
        (-1, u'last')
    ) 
    
    WEEKDAY_LONG = (
        (7, u'Sunday'),
        (1, u'Monday'),
        (2, u'Tuesday'),
        (3, u'Wednesday'),
        (4, u'Thursday'),
        (5, u'Friday'),
        (6, u'Saturday')
    )
    
    INTERVAL = (
        (1, u'each'),
        (2, u'every other'),
        (3, u'every third'),
        (4, u'every fourth'),
        (5, u'every fifth'),
        (6, u'every sixth'),
        (7, u'every seventh'),
        (8, u'every eighth'),
        (9, u'every ninth'),
        (10, u'every tenth'),
        (11, u'every eleventh'),
        (12, u'every twelfth'),
    )

    def rrule2text(self):

        freq = self._freq
        interval = self._interval
        wkst = self._wkst
        until = self._until
        count = self._count
        bymonth = self._bymonth
        byweekno = self._byweekno
        byyearday = self._byyearday
        byweekday = self._byweekday
        bynweekday = self._bynweekday
        byeaster = self._byeaster
        bymonthday = self._bymonthday
        bynmonthday = self._bynmonthday
        bysetpos = self._bysetpos
        byhour = self._byhour
        byminute = self._byminute
        bysecond = self._bysecond
        
        text_description = []
        if freq != MONTHLY:
            raise Rrule2textError, "rrule2text only works with monthly frequencies right now."        
            
        # Get the interval. "Each", "Every other", "Every third", etc.
        p_interval = rrule2text.INTERVAL[interval-1][1]
        text_description.append(p_interval)

        # bynweekday is a tuple of (weekday, week_in_month) tuples
        for rule_pair in bynweekday:

            # Get the ordinal.
            for ord in rrule2text.ORDINAL:
                if ord[0] == rule_pair[1]:
                    text_description.append(ord[1])
                    break
            #p_ordinal = rrule2text.ORDINAL[rule_pair[1]][1]
            #text_description.append(p_ordinal)

            #  Get the weekday name
            # import pdb; pdb.set_trace()
            p_weekday = weekday(rule_pair[0])
            name = rrule2text.WEEKDAY_MAP[unicode(p_weekday)]
            #p_weekday = rrule2text.WEEKDAY_LONG[rule_pair[0] == 7 and 1 or rule_pair[0]][1]
            text_description.append(name)
            
            # tack on "and interval" for the next item in the list
            text_description.extend([u"and", p_interval])

        # remove the last "and interval" because it's hanging off the end
        # TODO improve this
        text_description = text_description[:-2]
        
        if count != 0:
            text_description.extend([unicode(int2word(count).rstrip()), u"times"])
        elif until:
            text_description.extend([u"until", unicode(until)])
            
        return text_description


class rrule2textTests(unittest.TestCase):
	def setUp(self):
		pass
		
	def test_not_monthly(self):
	    testrr = rrule2text(WEEKLY, byweekday=MO, dtstart=datetime(2011, 8, 15), until=datetime(2012, 8, 15))
	    self.assertRaises(Rrule2textError, testrr.rrule2text)
		
	def test_monthly(self):
	    correct = [u"each", u"third", u"Friday", u"ten", u"times"]
	    testrr = rrule2text(MONTHLY, byweekday=FR(3), dtstart=datetime(2011, 8, 15), count=10)
	    self.assertListEqual(testrr.rrule2text(), correct)


if __name__ == '__main__':
	unittest.main()