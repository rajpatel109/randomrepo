import requests
from time import sleep
from bs4 import BeautifulSoup, Comment


def getSoupFromURL(url, suppressOutput=True, max_retry=3):
    """
    This function grabs the url and returns and returns the BeautifulSoup object
    """
    if not suppressOutput:
        print(url)

    num_attempts = 0
    while num_attempts < max_retry:
        try:
            num_attempts += 1
            r = requests.get(url)
            r.raise_for_status()
            return BeautifulSoup(r.text, "lxml")
        except requests.exceptions.HTTPError as http:
            print("ERROR - HTTP:", http)
            if http.errno == 500:
                sleep(5)
        except requests.exceptions.ConnectionError as connection:
            print("ERROR - Connection:", connection)
            return None
        except requests.exceptions.Timeout as timeout:
            print("ERROR - Timeout:", timeout)
        except requests.exceptions.TooManyRedirects as redir:
            print("ERROR - Bad URL:", redir)
            return None
        except requests.exceptions.RequestException as e:
            print("ERROR:", e)


def find_html_in_comment(soup):
    for element in soup.children:
        if isinstance(element, Comment):
            comment = str(element.string).strip()
            return BeautifulSoup(comment, 'lxml')
    return None
