import json
from urllib.request import Request, urlopen
import pandas as pd
import sys
from pyontutils.scigraph_client import Vocabulary
from pyontutils.scigraph_client import Graph
sgv = Vocabulary(basePath='http://localhost:9000/scigraph')
gv = Graph(basePath='http://localhost:9000/scigraph')

ExcelFile = sys.argv[1]
xl = pd.ExcelFile(ExcelFile)
print(xl.sheet_names)
df = xl.parse(xl.sheet_names[0])

label_index = [tag.lower() for tag in list(df.head())].index('label') # get column
labels = [label for label in list(df.iloc[:, label_index]) if type(label) != float] # make list with no empty cells
labels = list(map(str, labels)) # some where integers
atlas = {label:index for index, label in list(enumerate(labels))} # keep track of complete data
labels = [label for label in labels if 'Resource:' not in label] # Resource already has a home
labels = list(set(labels)) # take away repeats
print('Total # of labels:', len(labels))

labels = labels[0:15]

#FIXME should I also include pato?
def isNIF(ontologies):
    for ontology in ontologies:
        if 'nif' in ontology.lower():
            return True
    return False

memo = {}
url = 'http://data.bioontology.org/search?q='
API_KEY = '0140ff1b-bfc1-4427-bb8c-02ce36bbd586'
for label in labels:
    search = sgv.findByTerm(label)
    if search != []:
        iris = [search[i]['iri'] for i in range(len(search))]
        in_NIF = False
        ontologies = []
        for iri in iris:
            ontologies = [e['obj'] for e in gv.getNeighbors(iri)['edges'] if e['pred']=='isDefinedBy'] + ontologies
            if isNIF(ontologies):
                in_NIF = True
                break
        if not in_NIF:
            memo[label] = ontologies
            print('here', label)
    else:
        label_ = label.replace(' ', '%20')
        q = Request(url + label_)
        q.add_header('Authorization', 'apikey token=' + API_KEY)
        data = json.loads(urlopen(q).read())
        ontologies = set()
        for i in range(len(data['collection'])):
            ontologies.add(data['collection'][i]['links']['ontology'])
        memo[label]=list(ontologies)

output = open('labels4_NIF_update.json', 'w')
output.write(json.dumps(memo))
output.close()
