import requests
from sag import SAG
from bs4 import BeautifulSoup

def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Example usage
url = "https://openai.com/blog/governance-of-superintelligence"
html = get_html(url)
if html:
    # print(html)
    pass
else:
    print("Failed to acquire HTML from the URL.")


soup: BeautifulSoup = BeautifulSoup(html, features="lxml")


sag = SAG()
def gotree(node, depth=1, count=0):
    ct = 1
    for i in node:
        if i.name is None:
            continue
        ct += gotree(i, depth + 1)
        sag.score(i, ct)
    return ct

gotree(soup)
cleaned_soup = sag.get_content()

print(cleaned_soup)