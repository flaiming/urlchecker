import sys
import json

from url_checker import check_url, UrlStatus


if __name__ == "__main__":
    #url = sys.argv[1]
    #print url
    #print dict(UrlStatus.choices())[check_url(url)]

    choices = dict(UrlStatus.choices())

    with open('data.json') as f:
        data = json.load(f)
        for url, url_status in data:
            current_status = check_url(url)
            if current_status != url_status:
                print "%s status was %s and now is %s" % (url, choices[url_status], choices[current_status])


