from scrapingtools import get_all_global_links

#left off here: need to make sure we're getting links correctly; test get_all_links local and global
# versions against each other and manually inspect links inside small webpages


url = "https://stackoverflow.com/questions/19168220/scrape-internal-links-with-beautiful-soup"
url = "https://riverbend.appfolio.com/connect/users/sign_in"
url = "https://en.wikipedia.org/wiki/Affirmative_conclusion_from_a_negative_premise"
url = "https://github.com/Matt-Gracz?tab=repositories"
#raw_html = simple_get(url)
#html = parse_raw_html(raw_html)
#links = (html)
#x = [print(link) for link in links if str(link).startswith('/')]

local_links = get_all_global_links(url)
x = [print(link) for link in local_links]


