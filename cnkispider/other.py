# -*- coding: UTF-8 -*-
__author__ = 'zy'
__time__ = '2020/2/11 21:11'
from lxml import etree
from urllib import parse
class OtherSpider():
    def get_detail_url(url):
        urldata = parse.urlparse(url)
        result = parse.parse_qs(urldata.query)
        f_n = result['filename'][0]  # 由于返回的是数组
        d_c = result['DbCode'][0]
        d_n = result['dbname'][0]
        # 拼接url也有更好的方法
        # query = {"name": "walker", "age": 99}   d = parse.urlencode(query)
        data = {
            'dbcode': d_c,
            'dbname': d_n,
            'filename': f_n
        }
        detail_url = 'http://kns.cnki.net/KCMS/detail/detail.aspx?DbCode=CJFD&dbname=' + d_n + '&filename=' + f_n
        return detail_url

    def clean(text):
        text = ''.join(text)
        text = text.replace('\r', '')
        text = text.replace('\n', '')
        text = text.replace('\r\n', '')
        text = text.replace("space", "")
        text = text.replace(" ", "")
        # text =text.replace('; ','')
        text = text.replace(";;", ";")
        text = text.strip()
        return text
