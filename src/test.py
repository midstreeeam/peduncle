import requests

from bs4 import BeautifulSoup

from grader import Grader

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

G = Grader(html)
print(G.main_node.text)