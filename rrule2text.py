#!/usr/bin/env python
# encoding: utf-8
"""
rrule2text.py

Created by William Bert on 2011-08-12.
Copyright (c) 2011. All rights reserved.
"""

import sys
import os
import unittest
from datetime import datetime

# TODO Add i18n

import dateutil
from dateutil.rrule import * # gets DAILY, WEEKLY, MONTHLY, etc.
from dateutil.rrule import weekday
from dateutil.rrule import rrule as rr
from dateutil.relativedelta import relativedelta as rd

from int2word import int2word

        
class Rrule2textError(ValueError):
    pass

class rrule2text(rr): 
    """Provide methods that return natural language descriptions of a dateutil.rrule 
    (aka a recurrence rule). Useful for describing recurring events in a calendar or
    event app.
    
    `rr` 
    Recurrence rule to get a natural language description of.
    
    """
    
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

    def text(self, date_format="%B %d, %Y", time_format="%I:%M %p"):
        """Return a recurrence rule in plain English (or whatever language, once translation
        is supported. :)
        
        `date_format`
        An optional argument that specifies the format to print dates using strftime 
        formatting rules.
        
        `time_format`
        An optional argument that specifies the format to print times using strftime
        formatting rles.
        """
        
        dtstart = self._dtstart
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

            #  Get the weekday name
            p_weekday = weekday(rule_pair[0])
            name = rrule2text.WEEKDAY_MAP[unicode(p_weekday)]
            text_description.append(name)
            
            text_description.append("at")
            
            text_description.append(dtstart.strftime(time_format))
            
            # tack on "and interval" for the next item in the list
            text_description.extend(["and", p_interval])

        # remove the last "and interval" because it's hanging off the end
        # TODO improve this
        text_description = text_description[:-2]
        
        if count:
            text_description.append("%s %s" % (int2word(count).rstrip(), "times"))
        elif until:
            text_description.extend(["until", until.strftime(date_format)])
            
        return map(unicode, text_description)
        
    def __eq__(self, other):
        """Compare two rrule2text instances."""
        
        attrs = [
         '_byeaster',
         '_byhour',
         '_byminute',
         '_bymonth',
         '_bymonthday',
         '_bynmonthday',
         '_bynweekday',
         '_bysecond',
         '_bysetpos',
         '_byweekday',
         '_byweekno',
         '_byyearday',
         '_count',
         '_dtstart',
         '_freq',
         '_interval',
         '_timeset',
         '_tzinfo',
         '_until',
         '_wkst',
        ]
         
        for p in attrs:
            a = getattr(self, p)
            b = getattr(other, p)
            if a != b:
                return False
            
        return True
        
    def __ne__(self, other):
        return not (self == other)
    
class rrule2textTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_equals(self):
        r1 = rrule2text(DAILY, dtstart=datetime(2012, 8, 15))
        r2 = rrule2text(DAILY, dtstart=datetime(2012, 8, 15))
        self.assertTrue(r1==r2)
        
        r1 = rrule2text(DAILY, dtstart=datetime(2012, 8, 15), byweekday=MO)
        r2 = rrule2text(DAILY, dtstart=datetime(2012, 8, 15), byweekday=MO)
        self.assertTrue(r1==r2)
        
    def test_not_equals(self):
        r1 = rrule2text(DAILY, dtstart=datetime(2012, 8, 15))
        r2 = rrule2text(MONTHLY, dtstart=datetime(2012, 8, 15))
        self.assertFalse(r1==r2)
        
        r2 = rrule2text(DAILY, dtstart=datetime(2011, 8, 15))
        self.assertFalse(r1==r2)
        
        r1 = rrule2text(DAILY, dtstart=datetime(2012, 8, 15), byweekday=MO)
        r2 = rrule2text(DAILY, dtstart=datetime(2012, 8, 15), byweekday=TU)
        self.assertFalse(r1==r2)
        
        
    def test_not_monthly(self):
        testrr = rrule2text(DAILY, byweekday=MO, dtstart=datetime(2011, 8, 15), until=datetime(2012, 8, 15))
        self.assertRaises(Rrule2textError, testrr.text)

        testrr = rrule2text(WEEKLY, byweekday=MO, dtstart=datetime(2011, 8, 15), until=datetime(2012, 8, 15))
        self.assertRaises(Rrule2textError, testrr.text)

        testrr = rrule2text(YEARLY, byweekday=MO, dtstart=datetime(2011, 8, 15), until=datetime(2012, 8, 15))
        self.assertRaises(Rrule2textError, testrr.text)
        
        
    def test_monthly(self):
        correct = map(unicode, ["each", "third", "Friday", "at", "12:00 AM", "ten times"])
        testrr = rrule2text(MONTHLY, byweekday=FR(3), dtstart=datetime(2011, 8, 15), count=10)
        self.assertListEqual(testrr.text(), correct)
        
        correct = map(unicode, ["every other", "first", "Sunday", "at", "09:00 PM", "until", "August 15, 2012"])
        testrr = rrule2text(MONTHLY, interval=2, byweekday=SU(1), dtstart=datetime(2011, 8, 15, 21, 0, 0), until=datetime(2012, 8, 15))
        self.assertListEqual(testrr.text(), correct)

        correct = map(unicode, ["every other", "first", "Sunday", "at", "09:00 PM", "until", "08/15/2012"])
        self.assertListEqual(testrr.text(date_format="%m/%d/%Y"), correct)
        
        correct = map(unicode, ["every other", "first", "Sunday", "at", "21:00", "until", "August 15, 2012"])
        self.assertListEqual(testrr.text(time_format="%H:%M"), correct)


if __name__ == '__main__':
    unittest.main()