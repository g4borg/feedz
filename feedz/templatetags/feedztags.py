# -*- coding: utf-8 -*-
from django import template
from django.contrib.auth.models import User
from feedz.models import UserFeed, UserFeedFolder
from django.db.models.query import EmptyQuerySet
register = template.Library()

@register.filter
def userfeedz(value):
    if value:
        if isinstance(value, User) and value.is_authenticated() and value.is_active:
            return UserFeed.objects.filter( owner = value )
    return EmptyQuerySet()

@register.filter
def userfeedzfolders(value):
    if value:
        if isinstance(value, User) and value.is_authenticated() and value.is_active:
            return UserFeedFolder.objects.filter( owner = value )
    return EmptyQuerySet()
