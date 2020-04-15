from ak_converter import AKConverter
from ak_parser import AKParser
from graph_builder import GraphBuilder
from pathlib import Path
from floyd_warshall import FloydWarshall
import webbrowser
import urllib
import base64

def quote_url(url):
    """URL-encodes a string (either str (i.e. ASCII) or unicode);
    uses de-facto UTF-8 encoding to handle Unicode codepoints in given string.
    """
    return urllib.parse.quote(str(url).encode('utf-8'))


def find_shortest_paths():
    document_list = list(Path('./data/').glob('*.akml'))

    graph_builder = GraphBuilder()

    graph_builder.parse_documents(document_list)

    graph_finder = FloydWarshall()
    graph_finder.find(graph_builder.graph)
    paths = graph_finder.paths

    for i in paths:
        for j in paths:
            if paths[i][j]:
                if i != j:
                    print(f'Path from {i} to {j} = {list(paths[i][j])}')


def to_html():
    parser = AKParser()
    converter = AKConverter()
    data = parser.parse('./data/sample.akml')

    html = converter.to_html(data)

    url = "data:text/html;base64," + base64.b64encode(
        html.encode("utf-8")).decode("utf-8")

    webbrowser.open(url)


to_html()
find_shortest_paths()
