# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
    Unit Description

@author: g4b

LICENSE AND COPYRIGHT NOTICE:

Copyright (C) 2010 by  Gabor Guzmics, <gab(at)g4b(dot)org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
from feedz.models import Feed, UserFeed, UserFeedFolder
from django.db.models.aggregates import Count

def create_feed_for_user( user, url, title, folder = None ):
    if Feed.objects.filter(url=url).exists():
        feed = Feed.objects.get(url=url)
    else:
        feed = Feed( url = url )
        feed.save()
    userfeed = UserFeed( owner = user,
                         feed = feed,
                         title = title,
                         position = UserFeed.objects.filter( owner = user).filter( folder = folder ).count()+1,
                         folder = folder,
                         )
    return userfeed.save()

def create_folder_for_user( user, foldername, position=None):
    folder=UserFeedFolder( owner=user,
                    title=foldername,
                    position=position or UserFeedFolder.objects.filter(owner=user).count()+1 )
    folder.save()
    return folder

def get_public_feeds():
    q = Feed.objects.annotate(num_userfeeds=Count('userfeedz'))
    return q.filter(public=True).distinct('pk').order_by('-num_userfeeds')

def get_public_feeds_latest_update():
    return Feed.objects.filter(public=True).order_by('-date_updated')
