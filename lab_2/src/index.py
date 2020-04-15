import sys
sys.path.insert(0, '../../lab_1/src')

from pathlib import Path
from search_engine import SearchEngine

document_list = list(Path('../../lab_1/src/data/').glob('*.akml'))

engine = SearchEngine()

engine.load_documents(document_list)

query = ['best', 'actor']

print(f'Query is: `{" ".join(query)}`')

result = engine.query(query)
result = list(filter(lambda i: i[1] > 0, result))
result.sort(key=lambda i: i[1], reverse=True)

for doc, score in result:
    print(f'Score: {score:.05}\t Doc: {doc}')
