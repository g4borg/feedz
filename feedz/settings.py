# -*- coding: utf-8 -*-

from django.conf import settings
from datetime import datetime, timedelta

DATE_MINIMUM = getattr( settings, 'FEEDZ_DATE_MINIMUM', timedelta(minutes=5) )

