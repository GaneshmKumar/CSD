""" Built in imports """
from string import Template

""" Exteral imports """
from bs4 import BeautifulSoup
import requests

""" Dictionary to store url type keys """
URL_TYPES = {
    "BASE": "base",
    "STATUS": "status",
    "SOLUTIONS": "solutions"
}

""" Dictionary to store url templates """
URLS = {
    "base": "https://www.codechef.com",
    "status": Template("$base/status/$problem_code"),
    "solutions": Template("$status?page=$page&language=$language&status=$status_code&handle=&Submit=GO")
}

"""
returns a url of requested type
"""
def get_url(url_type, **params):
    if url_type == URL_TYPES['BASE']:
        return URLS[url_type]
    elif url_type == URL_TYPES['STATUS']:
        return URLS[URL_TYPES['STATUS']].substitute(base=get_url('base'), problem_code=params['problem_code'])
    elif url_type == URL_TYPES['SOLUTIONS']:
        return URLS[URL_TYPES['SOLUTIONS']].substitute(status=get_url('status', problem_code=params['problem_code']), page=params['page'], language=params['language'], status_code=params['status_code'])      

