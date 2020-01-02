#practice application based on https://realpython.com/python-web-scraping-practical-introduction
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def log_error(e):
    """
    In: e, any instantiation of a data-type that supports __str__
    Out:
        No output.
    Side effects:
        writes e.__str__() to the error log file for this module
    """
    with(open("error_log.txt", 'a')) as log:
        log.write(str(e)+'\n')



def simple_get(url):
    """
    In: 
        url: a string of the form http[s]://{}.{}/{}

    Out:
        SUCCESS:  Raw html of the resposne to making an HTTP GET request at url.
        ERROR:    Returns None

    Side effects:
        Logs an error message if ERROR occurs.
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


def get_all_link_refs(html, parent_url = None):
    """
    In:
        html:       a BeautifulSoup html object
        parent_url: optional argument to resolve links in the local domain to a global domain,
                    i.e., local_url ==> <parent_url>/<local_url>, where parent_url is of the form
                    http[s]://{}.{}/{}


    Out:
        SUCCESS: linkrefs, a string-list of linkrefs.  if parent_url is not None, then all links in
                 linkrefs will be of the form http[s]://{}.{}/{}
        ERROR:   An empty list
    """
    #ensure parent_url is the actual domain and not a webpage in the domain:
    if parent_url is not None:
        domain = parent_url[:parent_url.find("/", parent_url.rfind("."))]
    else:
        domain = None

    linkrefs = []




    try:
        #TODO: clean up this code; it's hard to read
        for link in [link.get('href') for link in html.find_all('a')]:
            if link is not None:
                if domain is not None:
                    if not link.startswith("http"):
                        print("link {}".format(link))
                        if not link.startswith("/"):
                            link = "/" + link
                        link = domain + link
                        
                linkrefs.append(link)
    except Exception as e:
        log_error(str(e))
        linkrefs = []
    finally:
        return linkrefs

def get_all_global_links(url, force_global = True):
    """
        In:
            url: string of webpage to scrape links from
            force_global: for links that are of a local domain, i.e., being with "/", resolve the
                          global link for it so we can use it outside of url's domain
        
        Out:
            SUCCESS:
                returns all of the links in the webpage at url
    """
    raw_html = simple_get(url)
    html = parse_raw_html(raw_html)
    return get_all_link_refs(html, url if force_global else None)
