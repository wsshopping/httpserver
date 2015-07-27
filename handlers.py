#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Shopping'

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio

from aiohttp import web

from coroweb import get, post
from apis import Page, APIValueError, APIResourceNotFoundError

from models import Media, Tag, next_id
from config import configs

json_head = {'errmsg':'success', 'errcode':0, 'totalCount':1}
dict_style = {'aq':['%����%'],'ds':['%����%'],'gz':['%��װ%'],'lz':['%��־%'],'qc':['%�ഺ%'],'kh':['%�ƻ�%'],'yx':['%Ժ��%'],'xj':['%ϲ��%']}

def create_json_head(count = 1, last_page = 0):
    if count and not last_page:
       json_head["errmsg"] = "success"
       json_head["errcode"] = 0
       json_head["totalCount"] = count

    elif count and last_page :
       json_head["errmsg"] = "success"
       json_head["errcode"] = -1000
       json_head["totalCount"] = count
    
    else:
       json_head["errmsg"] = "error"
       json_head["errcode"] = -1
       json_head["totalCount"] = count
    
    return json_head         

def is_last_page(total_count = 0, pagesize = 6): 
    if total_count < pagesize :
        return True
    else:
        return False

#��ȡ�Ȳ�ý��
@get('/flysee/getAssetHot')
def api_get_media_hot(request):
    num = request.GET.get('num') 
    curpage =  request.GET.get('curpage') 
    pagesize =  request.GET.get('pagesize') 
    total_count = 0
    last_page_or_not = 0
    print(curpage)
    print(pagesize)
    #��ҳ����
    if curpage and pagesize:
        curpage = int(curpage)
        pagesize = int(pagesize)

        offset = (curpage - 1) * pagesize
        dataList = yield from Media.getAssetHot(orderBy='hot desc', limit=[offset, pagesize])
        total_count = len(dataList)
        last_page_or_not = is_last_page(total_count, pagesize = pagesize)


    #��ҳ����
    else:
        if not num :
            num = 3;
        num = int(num)
        dataList = yield from Media.getAssetHot(orderBy='hot desc', limit=num)
        total_count = len(dataList)

    return dict(create_json_head(total_count, last_page_or_not), dataList=dataList)

#��ȡ�Ƽ�ý��
@get('/flysee/getAssetRecomment')
def api_get_media_recommend(request):
    type = request.GET.get('recommondtype') 
    id = request.GET.get('id') 
    total_count = 0
    #ý���Ƽ�ý��
    if type and id:
        id = int(id)
        if type == 'asset' :
            dataList = yield from Media.getAssetRecommend('id=?' ,id, type='asset')
            total_count = len(dataList)
    #��ҳý���Ƽ�
    else:
        if type == 'index' :
            dataList = yield from Media.getAssetRecommend("rmdposter<>'' ",args=None, type='index')
            total_count = len(dataList)
        else :
            raise APIValueError('getAssetRecomment', 'parse param error.')

    return dict(create_json_head(total_count),dataList=dataList)


#��ȡý������ҳ
@get('/flysee/getAssetDetail')
def api_get_media_detail(request):
    id = request.GET.get('id') 
    if id:
        id = int(id)
        dataList = yield from Media.getAssetDetail('id=?',id)
        total_count = len(dataList)
    else :
       raise APIValueError('getAssetDetail', 'parse param error id must > 0.')
    return dict(create_json_head(total_count),dataList=dataList)


#��ȡ��ǩ�б�
@get('/flysee/getTagList')
def api_get_media_tag(request):


    dataList = yield from Tag.getTagList()
    total_count = len(dataList)

    return dict(create_json_head(total_count),dataList=dataList)



#��ȡ��ǩ�е�ý���б�
@get('/flysee/getAssetList')
def api_get_media_taglist(request):

    querytype = request.GET.get('querytype')
    curpage =  request.GET.get('curpage')
    pagesize =  request.GET.get('pagesize')
    #Ĭ�ϲ������һҳ
    last_page_or_not = 0
    total_count = 0
    #��ҳ����
    if curpage and pagesize and querytype:
        curpage = int(curpage)
        pagesize = int(pagesize)

        offset = (curpage - 1) * pagesize

        print ("querytype is %s"%querytype)
        dataList = yield from Media.getAssetList('`style` like ?',dict_style[querytype],limit=(offset, pagesize))
        total_count = len(dataList)
        last_page_or_not = is_last_page(total_count, pagesize = pagesize)
  
    #Ĭ������
    else:
        curpage = 1
        pagesize = 3

        dataList = yield from Media.getAssetList(limit=num)
        total_count = len(dataList)
        last_page_or_not = is_last_page(total_count, pagesize = pagesize)
  

    return dict(create_json_head(total_count, last_page_or_not), dataList=dataList)


