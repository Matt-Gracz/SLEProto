from scrapingtools import simple_get, parse_raw_html, log_error, get_all_link_refs

raw_html = simple_get("https://stackoverflow.com/questions/19168220/scrape-internal-links-with-beautiful-soup")
html = parse_raw_html(raw_html)
links = get_all_link_refs(html)
x = [print(link) for link in links if str(link).startswith('/')]

