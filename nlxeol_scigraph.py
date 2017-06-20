import pandas as pd
import math
import subprocess as sb
from multiprocessing import Pool
import json
from pyontutils.scigraph_client import Vocabulary
from pyontutils.scigraph_client import Graph

sgv = Vocabulary(basePath='http://localhost:9000/scigraph')
gv = Graph(basePath='http://localhost:9000/scigraph')

xl = pd.ExcelFile("/Users/love/Desktop/nlxeol/neurolex_full.xls")
print(xl.sheet_names)
df = xl.parse(xl.sheet_names[0])

label_index = [tag.lower() for tag in list(df.head())].index('label')
labels = [label for label in list(df.iloc[:, label_index]) if type(label) != float]


labels = list(map(str, labels))
labels = [label for label in labels if 'Resource:' not in label]
labels = list(set(labels))
labels = list(enumerate(labels))
print('Total # of labels:', len(labels))

in_list = [v[1] for v in labels if sgv.findByTerm(v[1]) != []]
not_in_list = [v[1] for v in labels if len(sgv.findByTerm(v[1])) < 1]

out = open('labels_not_in_nlxeol.txt', 'w')
out.write('\n'.join(not_in_list))
out.close()

out = open('labels_in_nlxeol.txt', 'w')
out.write('\n'.join(in_list))
out.close()
