# -*- coding: utf-8 -*-
import logging
import requests
import oss2

fetchUrl = 'https://www.bing.com/HPImageArchive.aspx?format=js&n=1&mkt=zh-CN&idx=0'
baseUrl = 'https://cn.bing.com'

auth = oss2.Auth('<yourAccessKeyId>', '<yourAccessKeySecret>')
bucket = oss2.Bucket(auth, '<yourEndpoint>', '<yourBucketName>')


def fetch():
    res = requests.get(fetchUrl).json()
    data = res['images'][0]
    url = baseUrl + data['url']
    key = data['enddate']
    return key, url


def handler(event, context):
    logger = logging.getLogger()
    key, url = fetch()
    logger.info(key, url)
    bucket.put_object(key + '.jpeg', requests.get(url))
    return key, url
