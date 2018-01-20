""" Exteral imports """
from bs4 import BeautifulSoup
import requests
import json

""" Built in imports """
from string import Template

""" Custom imports """
import argparser


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

CONFIG_FILES = {
    "EXTENSIONS": "extensions.json",
    "LANGUAGE_CODES": "language_codes.json",
    "STATUS_CODES": "status_codes.json"
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

"""
return the soup data of the given url
"""
def get_url_data(url):
    r = requests.get(url)
    return BeautifulSoup(r.text)

"""
returns json file content
"""
def load_json_file(json_file):
    config_folder = 'config/'
    return json.load(open(config_folder + json_file))

if __name__ == "__main__":
    parser = argparser.init_parser()
    args = parser.parse_args()
    
    pages = args.p 
    languages = map(lambda x: x.upper(), args.l)
    status_codes = map(lambda x: x.upper(), args.sc)
    problem_code = args.pc.upper()

    extensions = load_json_file(CONFIG_FILES["EXTENSIONS"]) # .java, .c, etc ...
    language_codes = load_json_file(CONFIG_FILES["LANGUAGE_CODES"]) # JAVA, C, PERL, etc ...
    status_codes = load_json_file(CONFIG_FILES["STATUS_CODES"]) # AC, WA, TLE, etc ...

    
    
