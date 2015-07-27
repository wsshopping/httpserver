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
dict_style = {'aq':['%爱情%'],'ds':['%都市%'],'gz':['%古装%'],'lz':['%励志%'],'qc':['%青春%'],'kh':['%科幻%'],'yx':['%院线%'],'xj':['%喜剧%']}

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

#获取热播媒资
@get('/flysee/getAssetHot')
def api_get_media_hot(request):
    num = request.GET.get('num') 
    curpage =  request.GET.get('curpage') 
    pagesize =  request.GET.get('pagesize') 
    total_count = 0
    last_page_or_not = 0
    print(curpage)
    print(pagesize)
    #分页请求
    if curpage and pagesize:
        curpage = int(curpage)
        pagesize = int(pagesize)

        offset = (curpage - 1) * pagesize
        dataList = yield from Media.getAssetHot(orderBy='hot desc', limit=[offset, pagesize])
        total_count = len(dataList)
        last_page_or_not = is_last_page(total_count, pagesize = pagesize)


    #首页请求
    else:
        if not num :
            num = 3;
        num = int(num)
        dataList = yield from Media.getAssetHot(orderBy='hot desc', limit=num)
        total_count = len(dataList)

    return dict(create_json_head(total_count, last_page_or_not), dataList=dataList)

#获取推荐媒资
@get('/flysee/getAssetRecomment')
def api_get_media_recommend(request):
    type = request.GET.get('recommondtype') 
    id = request.GET.get('id') 
    total_count = 0
    #媒资推荐媒资
    if type and id:
        id = int(id)
        if type == 'asset' :
            dataList = yield from Media.getAssetRecommend('id=?' ,id, type='asset')
            total_count = len(dataList)
    #首页媒资推荐
    else:
        if type == 'index' :
            dataList = yield from Media.getAssetRecommend("rmdposter<>'' ",args=None, type='index')
            total_count = len(dataList)
        else :
            raise APIValueError('getAssetRecomment', 'parse param error.')

    return dict(create_json_head(total_count),dataList=dataList)


#获取媒资详情页
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


#获取标签列表
@get('/flysee/getTagList')
def api_get_media_tag(request):


    dataList = yield from Tag.getTagList()
    total_count = len(dataList)

    return dict(create_json_head(total_count),dataList=dataList)



#获取标签中的媒资列表
@get('/flysee/getAssetList')
def api_get_media_taglist(request):

    querytype = request.GET.get('querytype')
    curpage =  request.GET.get('curpage')
    pagesize =  request.GET.get('pagesize')
    #默认不是最后一页
    last_page_or_not = 0
    total_count = 0
    #分页请求
    if curpage and pagesize and querytype:
        curpage = int(curpage)
        pagesize = int(pagesize)

        offset = (curpage - 1) * pagesize

        print ("querytype is %s"%querytype)
        dataList = yield from Media.getAssetList('`style` like ?',dict_style[querytype],limit=(offset, pagesize))
        total_count = len(dataList)
        last_page_or_not = is_last_page(total_count, pagesize = pagesize)
  
    #默认请求
    else:
        curpage = 1
        pagesize = 3

        dataList = yield from Media.getAssetList(limit=num)
        total_count = len(dataList)
        last_page_or_not = is_last_page(total_count, pagesize = pagesize)
  

    return dict(create_json_head(total_count, last_page_or_not), dataList=dataList)


