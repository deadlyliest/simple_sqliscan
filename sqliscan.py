from urllib import parse
import copy
import sys
import requests



def request(url):
    headers = {"User-Agent" : "", "Cookie": ""}
    try:
        response = requests.get(url, headers=headers)
        html = response.text
        return html
    except:
        pass


def isvulnerable(html):
    errors = ["mysql_fetch_array()",
             "You have an error in your SQL syntax"]

    for error in errors:
        if error in html:
            return True


if __name__ == '__main__':
    url = sys.argv[1]
    url_parsed = parse.urlsplit(url)
    params = parse.parse_qs(url_parsed.query)
    for param in params.keys():
        query = copy.deepcopy(params)
        for c in "'\"":
            query[param][0] = c
            new_params = parse.urlencode(query, doseq=True)
            url_final = url_parsed._replace(query=new_params)
            url_final = url_final.geturl()
            html = request(url_final)
            if html:
                if isvulnerable(html):
                    print("VULNERABLE {}".format(param))
                    quit()

print("NOT VULNERABLE")
