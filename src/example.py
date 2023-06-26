import requests
from grader import Grader

def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Example usage
url = "https://blog.rust-lang.org/2023/05/29/RustConf.html"
html = get_html(url)

G = Grader(html)
print(G.main_node.text)