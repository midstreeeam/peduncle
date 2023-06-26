from bs4 import BeautifulSoup


class SAG:
    def __init__(self):
        self.nodelist = []
        pass

    def __get_text_length(self, node):
        text: str = node.text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        for i in range(20):
            text = text.replace("  ", " ")
        return len(text)

    def __score_text_children_ratio(self, child_count, text_length):
        # too much and too little children gets low score
        # more text higher the score
        c = child_count / 10
        c_score = c + 1 / c
        return text_length / c_score

    def __score_text_link_ratio(self, node, text_length):
        pass

    def __score_tag_name(self, node):
        a0 = ["article", "content", "tbody", "main", "body"]
        a1 = ["center"]

        b0 = [
            "script",
            "style",
            "noscript",
            "applet",
            "meta",
            "link",
            "a",
            "base",
            "img",
            "button",
        ]
        b1 = [
            "header",
            "footer",
            "aside",
            "tfoot",
            "menu",
            "nav",
            "frame",
            "iframe",
            "form",
            "title",
            "h1",
            "h2",
        ]

        if node.name in a0:
            return 3
        if node.name in a1:
            return 1.5

        if node.name in b0:
            return 0
        if node.name in b1:
            return 0.1

        return 1

    def _score(self, node, child_count):
        text_length = self.__get_text_length(node)

        child_score = self.__score_text_children_ratio(child_count, text_length)
        length_score = self.__score_text_link_ratio(node, text_length)
        tag_score = self.__score_tag_name(node)

        return child_score * tag_score

    def score(self, node, child_count):
        self.nodelist.append([node, self._score(node, child_count)])

    def get_content(self):
        self.nodelist = sorted(self.nodelist, key=lambda x: x[1], reverse=True)
        return self.nodelist[0][0]