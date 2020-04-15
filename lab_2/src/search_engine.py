from collections import deque
import re
from ak_parser import AKParser
from tfidf import TfIdf


class SearchEngine:
    def __init__(self):
        self.tfidf = TfIdf()

    def load_documents(self, documents):
        for doc in documents:
            name = doc.name
            text = self.doc_to_text(doc)
            words = self.text_to_word_array(text)

            self.tfidf.add_document(name, words)

    def query(self, query):
        return self.tfidf.similarities(query)

    def doc_to_text(self, doc):
        parser = AKParser()
        tree = parser.parse(doc)

        text = ''

        q = deque()
        q.append(tree)

        while True:
            if not q:
                break

            node = q.pop()

            if node.tag:
                if 'link' == node.tag.lower():
                    val = node.children[0].value.split('|')[0]
                    text += f' {val} '
                    continue

            if node.value:
                text += f' {node.value} '

            children = node.children

            if children:
                for c in children:
                    q.append(c)

        return re.sub(' +', ' ', text)

    def text_to_word_array(self, text):
        regex = re.compile('[^a-zA-Z\s]')

        text = regex.sub('', text)
        text = re.sub(' +', ' ', text)

        return text.lower().split()
