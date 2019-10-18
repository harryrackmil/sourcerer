import time

from sourcerer.scraper.bs_utils import get_soup

URL_SUBSTRING_BLACKLIST = [
    "video",
    "mailto",
    "watch"
]

def contains_blacklisted_substring(link):
    for url_substring in URL_SUBSTRING_BLACKLIST:
        if url_substring in link:
            return True
    return False

def filter_irrelevant_links(links):
    unblacklisted_links = filter(lambda l: not contains_blacklisted_substring(l), links)
    return unblacklisted_links

def scrape_links_from_homepage(homepage_url, max_links = 500, sleep=0):
    links = bfs_links(homepage_url, homepage_url, max_links, sleep)
    return links

def get_all_internal_links(url, domain):
    page = get_soup(url)
    links = [link.get("href") for link in page.findAll('a')]
    if links is not None:
        absolute_internal_links = filter(lambda l: l is not None and domain in l, links)
        relative_internal_links = filter(lambda l: l is not None and len(l) > 0 and l[0] == "/", links)
        absolutized_relative_links = [domain + link for link in relative_internal_links]
        all_links = absolute_internal_links + absolutized_relative_links
        relevant_links = filter_irrelevant_links(all_links)
        normalized_links= map(normalize_url, relevant_links)
        return normalized_links
    else:
        return []

def remove_trailing_slash(url):
    if url[-1] == "/":
        return url[:-1]
    return url

def remove_section_from_url(url):
    if url.find("#") > -1:
        return url[:url.find("#")]
    return url

def normalize_url(url):
    url = remove_trailing_slash(url)
    url = remove_section_from_url(url)
    url = url.lower()
    return url


def bfs_links(domain, entry_point_url, max_links = 500, sleep=0):

    visited_pages = set([])
    queue = [normalize_url(entry_point_url)]

    while len(queue) > 0 and len(visited_pages) < max_links:
        child = queue.pop(0)
        if child not in visited_pages:
            queue += get_all_internal_links(child, domain)
            visited_pages.add(child)
            time.sleep(sleep)

    return visited_pages
