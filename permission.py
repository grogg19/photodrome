# -*- coding: utf8 -*-
import datetime


s = str(datetime.datetime.timestamp(datetime.datetime.now()))
s = s.replace('.', '')
print(s)