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
from django.db import models
from datetime import datetime, timedelta
from gdjet.models.fields import JSONField
from fparser import feedparser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import settings
from feedz.fetchfeed import FeedzJSONEncoder

class FeedManager(models.Manager):
    def get_query_set(self):
        return super(FeedManager, self).get_query_set(
                    ).filter( 
                        public = True 
                    )

class Feed( models.Model ):
    title = models.CharField(_("Title"), blank = True, null = True, max_length = 400 )
    url = models.URLField(_("URL"), unique = True )
    date_updated = models.DateTimeField(_("Date Updated"), default = datetime.now )
    #date_created = models.DateTimeField(_("Date Created"), auto_add_now=True )
    data = JSONField(_("Feed Data"), default = None, null = True, blank = True,
                     json_encoder=FeedzJSONEncoder )
    public = models.BooleanField( default = True, blank = True )
    
    objects = models.Manager()
    pub_objects = FeedManager()
    
    def update_feed(self, force = False):
        try:
            if not self.pk or force or (datetime.now() - self.date_updated) > settings.DATE_MINIMUM: 
                try:
                    feed = feedparser.parse(self.url )
                except:
                    feed = None
            if feed:
                self.data = dict( feed )
                if not self.title:
                    self.title = feed['feed'].get('title', self.url )
                self.date_updated = datetime.now()
            return self.data
        except Exception, e:
            print "Exception in update_feed %s" % e
            return None
    
    def save(self, *args, **kwargs):
        self.update_feed()
        super( Feed, self ).save(*args, **kwargs)
    
    def get_link(self):
        try:
            return self.data['feed']['link']
        except:
            return ''
    link = property(get_link)
    
    def get_version(self):
        try:
            return self.data['version']
        except:
            return 'unknown'
    version = property(get_version)
    
    def get_count(self):
        try:
            return len( self.data['entries'] )
        except:
            return 0
    count = property( get_count )
    
    def __unicode__(self):
        return u"%s %s %s" % ( self.get_version(), self.title, self.url )

class UserFeedFolder( models.Model ):
    owner = models.ForeignKey( User, related_name = 'feedz_folders')
    title = models.CharField( _("Title"), max_length = 40 )
    position = models.IntegerField( _("Position"), default = 0 )
    def get_count(self):
        try:
            return self.feedz.count()
        except:
            return 0
    count = property( get_count )
    class Meta:
        ordering = ['position']
    def __unicode__(self):
        return u"%s" % self.title

class UserFeedManager(models.Manager):
    def get_query_set(self):
        return super(UserFeedManager, self).get_query_set()

class UserFeed( models.Model ):
    owner = models.ForeignKey( User, related_name='feedz' )
    feed = models.ForeignKey( Feed, related_name='userfeedz', blank = True, null = True )
    date = models.DateTimeField( default=datetime.now )
    title = models.CharField( _("Title"), max_length=200 )
    position = models.IntegerField( default=0, blank=True )
    folder = models.ForeignKey( UserFeedFolder, null=True, blank=True, related_name = 'feedz' )
    
    def get_data(self):
        try:
            return self.feed.data
        except:
            return None
    
    def __unicode__(self):
        return u"%s: %s" %( self.owner, self.feed )
    
    class Meta:
        ordering = ['folder', 'position']

#class UserPrivateFeed():
# # Private Feeds do not cache data. They do not register a feed object.
