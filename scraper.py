import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

ics_disallow = r"^/bin/.*|^/~mpufal/.*"
cs_disallow = r"^/wp-admin/.*"
stat_disallow = r"^/wp-admin/.*"
informatics_disallow = r"^/wp-admin/.*|^/research/.*"
informatics_allow = (r"^/wp-admin/admin-ajax.php|^/research/labs-centers/.*|^/research/areas-of-expertise/.*"
                    r"^/research/example-research-projects/.*|^/research/phd-research/.*|^/research/past-dissertations/.*"
                    r"^/research/masters-research/.*|^/research/undergraduate-research/.*|^/research/gifts-grants/.*")

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    num_unique_link = 0 # To count number of unique links
    url_set = set() #List with hyperlink to return

    if 200 <= resp.status < 300 : #if status code is ok and it is a valid link
        soup = BeautifulSoup(resp.raw_response.content, 'lxml') #parser using beautiful soup
        for link in soup.find_all('a'):
            extracted_url = link.get('href')
            index = extracted_url.rfind('#')
            url_remove_fragment = extracted_url[:index] if index >= 0 else extracted_url #removes the fragment portion of url
            url_set.add(url_remove_fragment) #adds url to list

    return list(set(url_set))
    #return list()

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if check_robots(parsed):
            return not re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
        else:
            return False
    except TypeError:
        print ("TypeError for ", parsed)
        raise

def check_robots(url):
    # checks if the url is under one of the four domains and is disallowed by their robots.txt

    netloc = url.netloc.lower()
    path = url.path.lower()

    if re.match(r".*.ics.uci.edu.*", netloc):
        return not re.match(ics_disallow, path)
    if re.match(r".*.cs.uci.edu.*", netloc):
        return re.match(r"^/wp-admin/admin-ajax.php", path) or not re.match(cs_disallow, path) 
    if re.match(r".*.stat.uci.edu.*", netloc):
        return re.match(r"^/wp-admin/admin-ajax.php", path) or not re.match(stat_disallow, path)
    if re.match(r".*.informatics.uci.edu.*", netloc):
        return re.match(informatics_allow, path) or not re.match(informatics_disallow, path)
    return False

