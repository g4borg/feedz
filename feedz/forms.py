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

from django import forms
from django.forms.models import BaseModelFormSet, modelformset_factory
from feedz.models import UserFeed, UserFeedFolder, Feed
from django.utils.translation import ugettext_lazy as _

class FeedForm(forms.Form):
    title = forms.CharField( max_length = 200 )
    url = forms.URLField( verify_exists = True )

class FeedFormFolder(forms.Form):
    def __init__(self, *args, **kwargs ):
        user = None
        if kwargs.has_key('user'):
            user = kwargs['user']
            del kwargs['user']
        else:
            raise RuntimeError, "FeedFormFolder needs user as Variable"
        super(FeedFormFolder, self).__init__( *args, **kwargs )
        self.fields['folder'].queryset = UserFeedFolder.objects.filter( owner=user )
    title = forms.CharField( max_length = 200 )
    url = forms.URLField( verify_exists = True )
    folder = forms.ModelChoiceField(queryset=UserFeedFolder.objects.none(), required=False)

class UserFolderForm( forms.Form ):
    title = forms.CharField( max_length = 40 )

class BaseUserFeedFormSet(BaseModelFormSet):
    def add_fields(self, form, index):
        super(BaseUserFeedFormSet, self).add_fields(form, index)
        form.fields["marked"] = forms.BooleanField(required = False)

FormsetUserFeeds = modelformset_factory(UserFeed, formset=BaseUserFeedFormSet, fields=('marked','title',), extra=0)

class BaseUserFeedFolderFormSet(BaseModelFormSet):
    def add_fields(self, form, index):
        super(BaseUserFeedFolderFormSet, self).add_fields(form, index)
        form.fields["marked"] = forms.BooleanField(required = False)

FormsetUserFeedFolders = modelformset_factory(UserFeedFolder, formset=BaseUserFeedFolderFormSet, fields=('marked','title',), extra=0)

