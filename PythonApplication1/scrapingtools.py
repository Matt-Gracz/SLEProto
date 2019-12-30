#practice application based on https://realpython.com/python-web-scraping-practical-introduction
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    In: e, any instantiation of a data-type that supports __str__
    Out:
        None
    Side effects:
        writes e.__str__() to the error log file for this module
    """
    with(open("error_log.txt", 'a')) as log:
        log.write(str(e)+'\n')

def parse_raw_html(raw_html):
    """
    In:
        raw_html: a string of potentially-parsable raw html code
    Out:
        SUCCESS:  string raw_html as a BeautifulSoup html object
        ERROR:    None
    """
    try:
        html = BeautifulSoup(raw_html, 'html.parser')
    except Exception as e:
        log_error(str(e))
        html = None
    finally:
        return html

def get_all_link_refs(html):
    """
    In:
        html:    a BeautifulSoup html object

    Out:
        SUCCESS: linkrefs, a string-list of linkrefs of the form http[s]://{}.{}/{}
        ERROR:   An empty list
    """
    linkrefs = []
    try:
        for link in [link.get('href') for link in html.find_all('a')]:
            linkrefs.append(link)
    except Exception as e:
        pass
    finally:
        return linkrefs