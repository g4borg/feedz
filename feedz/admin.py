# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
    Unit Description

@author: g4b

Copyright (C) 2010 by  Gabor Guzmics, <gab(at)g4b(dot)org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from django.contrib import admin
from feedz.models import *

class FeedAdmin( admin.ModelAdmin ):
    list_display = ( 'title', 'url', 'date_updated', 'link', 'version', 'count' )

class UserFeedAdmin(admin.ModelAdmin):
    list_display = ('owner', 'feed', )
    
class UserFeedFolderAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'count' )
    
admin.site.register( Feed, FeedAdmin )
admin.site.register( UserFeed, UserFeedAdmin )
admin.site.register( UserFeedFolder, UserFeedFolderAdmin )
