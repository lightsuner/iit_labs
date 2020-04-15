import math
from collections import deque

from ak_parser import AKParser


class GraphBuilder:
    def __init__(self):
        self.graph = {}

    def parse_documents(self, document_list):
        self.init_graph(document_list)

        processed_docs = self.process_docs(document_list)

        self.build_graph(processed_docs)

    def init_graph(self, documents):
        for i in documents:
            r = {}
            for j in documents:
                if i.name == j.name:
                    r[j.name] = 0
                else:
                    r[j.name] = math.inf

            self.graph[i.name] = r

    def process_docs(self, documents):
        processed_docs = {}

        parser = AKParser()
        for p in documents:
            processed_docs[p.name] = parser.parse(p)

        return processed_docs

    def build_graph(self, parsed_docs):
        for n, lang_tree in parsed_docs.items():
            link_values = self.get_link_values(lang_tree)

            for lv in link_values:
                if n in self.graph:
                    if lv in self.graph[n]:
                        if n != lv:
                            self.graph[n][lv] = 1

    def get_link_values(self, lang_tree):
        link_values = []
        q = deque()
        q.append(lang_tree)

        while True:
            if not q:
                break

            node = q.pop()

            if node.tag:
                if 'link' == node.tag.lower():
                    link_values.append(self.get_link(node))

            children = node.children

            if children:
                for c in children:
                    q.append(c)

        return link_values

    def get_link(self, node):
        link_value = ''
        ch = node.children

        if ch and len(ch) > 0:
            v = ch[0].value.split('|')
            link_value = v[1] if len(v) > 1 else v[0]

        return link_value.strip()
