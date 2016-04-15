import requests
import re


class UrlStatus(object):
    UNKNOWN = 0
    OK = 1
    ERROR = 2
    MOVED = 3
    PARKING = 4
    INVALID_URL = 5

    @classmethod
    def choices(cls):
        return (
            (cls.UNKNOWN, "unknown"),
            (cls.OK, "ok"),
            (cls.ERROR, "not working"),
            (cls.MOVED, "site moved"),
            (cls.PARKING, "parking site"),
            (cls.INVALID_URL, "invalid URL"),
        )

SEARCH_PHRASES = (
    r'godaddy\.com/park',
    r'(?:domain|website)\s+(?:name)?\s*(?:is)?\s*for\s+sale',
    r'buy\s+this\s+domain',
    r'sedoparking\.com',
    r'registrar_frameset',
    r'domain\s+has\s+expired',
    r'domain\s+(?:is)?\s*\s*parked',
)
MIN_WEBSITE_SIZE = 500  # Minimal webpage size in bytes


def same_domain(url1, url2):
    # cut out everything after third slash
    protocol1, domain1 = filter(lambda x: x, url1.split('/'))[:2]
    protocol2, domain2 = filter(lambda x: x, url2.split('/'))[:2]
    # normalize domains
    if domain1.startswith('www.'):
        domain1 = domain1[4:]
    if domain2.startswith('www.'):
        domain2 = domain2[4:]
    # normalize protocols
    if protocol1 == 'https:':
        protocol1 = 'http:'
    if protocol2 == 'https:':
        protocol2 = 'http:'
    return protocol1 == protocol2 and domain1 == domain2


def url_valid(url):
    if not isinstance(url, basestring):
        return False
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return regex.match(url)


def check_url(url, timeout=8):
    if not url_valid(url):
        return UrlStatus.INVALID_URL
    data = ""
    try:
        res = requests.get(url, timeout=timeout, headers={'user-agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"})
    except requests.exceptions.RequestException:
        return UrlStatus.ERROR

    if res.status_code != 200:
        return UrlStatus.ERROR

    data = res.text

    udata = re.sub(r'\s+', ' ', data)
    if len(udata) < MIN_WEBSITE_SIZE:
        return UrlStatus.PARKING

    for phrase in SEARCH_PHRASES:
        if re.search(phrase, data, flags=re.I) is not None:
            return UrlStatus.PARKING

    if res.history:
        for history in res.history:
            if not same_domain(url, history.url):
                return UrlStatus.MOVED

    return UrlStatus.OK
