import pandas as pd
import math
import subprocess as sb
from multiprocessing import Pool
from pyontutils.scigraph_client import Vocabulary
sgv = Vocabulary(basePath='http://localhost:9000/scigraph')
'''
git clone https://github.com/SciCrunch/SciGraph;
cd SciGraph \
git checkout example \
mvn -DskipTests -DskipITs install \
cd SciGraph-core \
mvn exec:java -Dexec.mainClass="io.scigraph.owlapi.loader.BatchOwlLoader" -Dexec.args="-c ../exampleGraph.yaml" \
cd ../SciGraph-services \
mvn exec:java -Dexec.mainClass="io.scigraph.services.MainApplication" -Dexec.args="server ../exampleServices.yaml" \

python3 scig.py -l s "some term" #you need it outside pyontutils because i didnt put it into PATH

Short version: take the labels in nlxeol/neurolex_full.csv and see if you can find terms from ontologies that
are not in the nif ontology that they map to.
'''

xl = pd.ExcelFile("/Users/love/Desktop/nlxeol/neurolex_full.xls")
print(xl.sheet_names)
df = xl.parse(xl.sheet_names[0])

label_index = [tag.lower() for tag in list(df.head())].index('label')
labels = [label for label in list(df.iloc[:, label_index]) if type(label) != float]

#check
nans = [label for label in list(df.iloc[:, label_index]) if type(label) == float]
[print('crap') for value in nans if math.isnan(value) == False]
print(len(labels))
labels = list(map(str, labels))
labels = list(enumerate(labels))

write_n = open('labels_not_in_NIF.txt', 'w')
#write_n = open('labels_in_NIF.txt', 'w')

def worker(label):
    count = label[0]
    label = label[1]

    if type(label) == str:
        label_bash_ready = ''.join(label.replace('(', '\(').replace(')', '\)'))
    else:
        label_bash_ready = str(label)

    #output = sb.getoutput('python3 scig.py -l s '+label_bash_ready)
    #iris = [value.split()[1] for value in output.split('\n') if 'iri:' in value]
    iris = [query['iri'] for query in sgv.searchByTerm(label)]
    if iris == []: iris = [query['iri'] for query in sgv.findByTerm(label)]

    if count % 5 == 0: print(count)

    if 'NIF' not in ''.join(iris) and iris != []:
        return label

    else:
        return '$'

p = Pool()
no_list = p.map(worker, labels)
print('length of list:', len(no_list))
for value in no_list:
    if value == '$': continue
    write_n.write(value+ '\n')

write_n.close()
