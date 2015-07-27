#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Models for user, blog, comment.
'''

__author__ = 'Shopping'

import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class Tag(Model):
    __table__ = 'taglist'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    estyle = StringField(ddl='varchar(50)')
    cstyle = StringField(ddl='varchar(50)')
    colour = StringField(ddl='varchar(50)')
    tagimg = StringField(ddl='varchar(200)')

class Media(Model):
    __table__ = 'video'

    
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    url	     = 	StringField(ddl='varchar(200)')
    hot      = 	StringField(ddl='varchar(15)')
    title    = 	StringField(ddl='varchar(200)')
    actor    = 	StringField(ddl='varchar(300)')
    director = 	StringField(ddl='varchar(200)')
    years    = 	StringField(ddl='varchar(100)')

    style    = 	StringField(ddl='varchar(50)')
    poster   = 	StringField(ddl='varchar(300)')
    profile  = 	StringField(ddl='varchar(1000)')
    rmdposter=  StringField(ddl='varchar(200)')
    #platform = 	StringField(ddl='varchar(200)')
    type     = 	StringField(ddl='varchar(10)')

