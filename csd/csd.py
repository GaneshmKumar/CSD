""" Exteral imports """
from bs4 import BeautifulSoup
import requests

""" Built in imports """
from string import Template
from os.path import expanduser
import sys
import re
import os

""" Custom imports """
from exception import ProblemNotFoundException
from exception import InvalidLanguageException
from exception import InvalidStatusException
import argparser

extensions = {"ADA":".ada","ASM":".asm","BASH":".bash","BF":".bf","C":".c","CAML":".ml","CLOJ":".clj","CLPS":".clp","COB":".cob","C++_4.3.2":".cpp","C++_6.3":".cpp","C++14":".cpp","C#":".cs","D":".d","ERL":".erl","FORT":".f","F#":".fs","GO":".go","HASK":".hs","ICK":".i","ICON":".icn","JAVA":".java","JS":".js","KOTLIN":".kt","LISP_CLISP":".lsp","LISP_SBCL":".lsp","LUA":".lua","NEM":".n","NICE":".nice","NODEJS":".js","PAS_FPC":".ps","PAS_GPC":".ps","PERL":".pl","PERL6":".pl","PHP":".php","PIKE":".pike","PRLG":".pro","PYPY":".py","PYTH":".py","PYTH_3.5":".py","RUBY":".rb","RUST":"rs","SCALA":".scala","SCM_CHICKEN":".scm","SCM_GUILE":".scm","SCM_QOBI":".scm","ST":".st","SWIFT":".swift","TCL":".tcl","TEXT":".txt","WSPC":".WSPC"}
language_codes = {"ALL":"All","ADA":7,"ASM":13,"BASH":28,"BF":12,"C":11,"CAML":8,"CLOJ":111,"CLPS":14,"COB":118,"C++_4.3.2":41,"C++_6.3":1,"C++14":44,"C#":27,"D":20,"ERL":36,"FORT":5,"F#":124,"GO":114,"HASK":21,"ICK":9,"ICON":16,"JAVA":10,"JS":35,"KOTLIN":47,"LISP_CLISP":32,"LISP_SBCL":31,"LUA":26,"NEM":30,"NICE":25,"NODEJS":56,"PAS_FPC":22,"PAS_GPC":2,"PERL":3,"PERL6":54,"PHP":29,"PIKE":19,"PRLG":15,"PYPY":99,"PYTH":4,"PYTH 3.5":116,"RUBY":17,"RUST":93,"SCALA":39,"SCM_CHICKEN":97,"SCM_GUILE":33,"SCM_QOBI":18,"ST":23,"SWIFT":85,"TCL":38,"TEXT":62,"WSPC":6}
status_codes = {"ALL":"All","AC":15,"WA":14,"TLE":13,"RTE":12,"CTE":11}

""" Dictionary to store url type keys """
URL_TYPES = {
    "BASE": "base",
    "STATUS": "status",
    "SOLUTIONS": "solutions"
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
    URLS = {
        "base": "https://www.codechef.com",
        "status": Template("$base/status/$problem_code"),
        "solutions": Template("$status?page=$page&language=$language&status=$status_code&handle=&Submit=GO")
    }

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
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)
    if len(r.history) == 1:
        try:
            raise ProblemNotFoundException("Error: There is no problem with the given code")
        except ProblemNotFoundException, e:
            print ''.join(e.args)
            sys.exit()
    return BeautifulSoup(r.text, "html.parser")

def is_solutions_not_available(data):
    return str(data).find('No Recent Activity') > -1

def get_total_solution_pages(data):
    page_info = data.find("div", {"class": "pageinfo"})
    if is_solutions_not_available(data):
        return 0
    elif page_info == None:
        return 1
    else:
        return int(page_info.text.split('of')[1])

def get_user_names(solutions_table):
    user_link_tags = [a for a in solutions_table.findAll("a", {"href": re.compile("/users/*")})]
    user_links = [link_tag['href'] for link_tag in user_link_tags]
    user_names = [link.split('/')[2] for link in user_links]
    return user_names

def get_solution_links(solutions_table):
    solution_link_tags = [a for a in solutions_table.findAll("a", {"href": re.compile("/viewsolution/*")})]
    solution_links = [link_tag['href'] for link_tag in solution_link_tags]
    return solution_links

def get_solution_languages(solutions_table):
    table_rows = solutions_table.findAll('tr')
    solution_languages = []
    for row in table_rows:
        td = row.findAll('td')
        if len(td) > 0:
            solution_languages.append('_'.join(td[6].text.split(' ')))
    return solution_languages

def get_solution_details(data):
    solutions_table = data.find("table", {"class": "dataTable"})
    user_names = get_user_names(solutions_table)
    solution_links = get_solution_links(solutions_table)
    solution_languages = get_solution_languages(solutions_table)
    return {"user_names": user_names, "solution_links": solution_links, "solution_languages": solution_languages}

def extract_solution_code(data):
    ol = data.find("div", {"id": "solutiondiv"}).find('ol')
    codes_list = []
    if ol:
        codes_list = ol.findAll('li')
    
    return '\n'.join([code_line.text for code_line in codes_list]).encode('utf-8').strip()

def save_solution(solution_code, solution_id, user_name, extension, problem_code, language, status):
    HOME_DIR = expanduser("~") 
    PROBLEM_DIR = HOME_DIR + '/Codechef_Solution_Downloader/' + problem_code + '/' + extension.split('.')[1] + '/' + status
    problem_file = os.path.normpath(PROBLEM_DIR + '/' + user_name + '_' + solution_id + extension)
    if not os.path.isdir(PROBLEM_DIR):
        os.makedirs(PROBLEM_DIR)

    with open(problem_file, 'w') as file_handle:
        print "Writing solution to the file " + problem_file
        file_handle.write(solution_code)

def download_solutions(solution_links, user_names, solution_languages, problem_code, language, status, extensions):
    base_url = get_url(URL_TYPES['BASE'])
    print "Downloading " + status + " solutions for " + problem_code
    for i in range(0, len(solution_links)):
        url = base_url + solution_links[i]
        data = get_url_data(url)
        solution_code = extract_solution_code(data)
        save_solution(solution_code, solution_links[i].split('/')[2], user_names[i], extensions[solution_languages[i]], problem_code, language, status)
        
def get_solutions(pages, languages, status, problem_code, language_codes, status_codes, extensions):
    try:
        for lang_key in languages:
            if lang_key not in language_codes:
                raise InvalidLanguageException("Error: There is no language named " + lang_key)
            for status_key in status:
                if status_key not in status_codes:
                    raise InvalidStatusException("Error: There is no status named " + status_key)
                if pages == -1:
                    url = get_url(URL_TYPES['SOLUTIONS'], problem_code=problem_code, language=language_codes[lang_key], status_code=status_codes[status_key], page=0)
                    data = get_url_data(url)
                    total_pages = get_total_solution_pages(data)
                else:
                    total_pages = pages
                
                for page in range(0, total_pages):
                    url = get_url(URL_TYPES['SOLUTIONS'], problem_code=problem_code, language=language_codes[lang_key], status_code=status_codes[status_key], page=page)
                    print "Getting solutions from " + url
                    data = get_url_data(url)
                    if get_total_solution_pages(data) == 0:
                        total_pages = 0
                        break
                    solution_details = get_solution_details(data)
                    download_solutions(solution_details["solution_links"], solution_details["user_names"], solution_details["solution_languages"], problem_code, lang_key, status_key, extensions)
                if total_pages == 0:
                    print "Getting solutions from " + url
                    print "No " + status_key + " solutions available in " + lang_key
    except (ProblemNotFoundException, InvalidLanguageException, InvalidStatusException) as e:
        print ''.join(e.args)
        sys.exit()                

def main():
    parser = argparser.init_parser()
    args = parser.parse_args()

    pages = args.p 
    languages = map(lambda x: x.upper(), args.l)
    status = map(lambda x: x.upper(), args.sc)
    problem_code = args.pc.upper()

    get_solutions(pages, languages, status, problem_code, language_codes, status_codes, extensions)

if __name__ == "__main__":
    main()
    