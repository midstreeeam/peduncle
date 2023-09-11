# peduncle

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/midstreeeam/peduncle/publish.yml)
![PyPI](https://img.shields.io/pypi/v/peduncle)
[![Downloads](https://static.pepy.tech/badge/peduncle)](https://pepy.tech/project/peduncle)

very very very simple DOM based HTML content extraction tool, get rid of boilerplate dressing of a web page[1].

easy but useable

work with python 3.7+



[1] the word comes from [dragnet](https://github.com/dragnet-org/dragnet).

## install

```shell
pip install peduncle
```

## usage

```Python
import requests
from peduncle.peduncle import extract_text

# obtain the raw html
url="https://blog.rust-lang.org/2023/05/29/RustConf.html"
html = requests.get(url).text

# extract
print(extract_text(html))
```

## benchmark

### data

benchmark data comes from [dragnet_data](https://github.com/seomoz/dragnet_data), which contains 1381 web pages.

### result

|        | similarity         | 95%hit_rate | avg_length_gap(char) | length_gap_std     |
| ------ | ------------------ | ----------- | -------------------- | ------------------ |
| a=0.01 | 0.5767456743946341 | 0.22        | -4673.118            | 15343.704819895227 |
| a=025  | 0.8451692708814662 | 0.548       | -2082.988            | 14502.183923390849 |
| a=0.5  | 0.8226224698726087 | 0.47        | -368.696             | 8452.075615349402  |
| a=0.99 | 0.7527591593485807 | 0.292       | 1614.306             | 7917.618208044891  |

- a: alpha, control how much the content extractor tens to extract larger content piece
- similarity: cosine similarity between sparse vectors of answer and extracted text
- 95hit rate: percentage of similarity larger than 95%
- length gap: extracted text length - answer text length
- std: std

## algorithm

Node grading is based on several key features:

- **tag name:** The tag name is a crucial determinant of a node's potential to contain the "main content". Nodes tagged with `<content>`, `<article>`, or `<main>` are more likely to house the main content than those tagged with `<menu>`, `<nav>`, or `<aside>`.

- **children tags:** The distribution of a node's child tags can also suggest its likelihood of being the main content. Nodes with a higher percentage of `<p>` tags among child tags are scored favorably.

- **text - children ratio:** Nodes with an excessively high or low number of children, or those with too much or too little text, are less likely to contain the main content — they're located too high or too low in the HTML tree. We thus use the text-to-children ratio to assess the suitability of a node, aiming for nodes that contain only a few sizable blocks of text.

  We use the following equation to calculate this ratio:
  
  $$\frac{t\times(1+c/n)}{c/n}$$
  
  Here, $t$ is the text length, $c$ is the total number of child nodes, and $n$ is a variable used to gauge what counts as "too few children". The $n$ variable is also instrumental in adjusting whether we want the chosen node to be closer to the root or leaf.

We recursively grade each node in the HTML tree and ultimately select one node per document as the main content.
