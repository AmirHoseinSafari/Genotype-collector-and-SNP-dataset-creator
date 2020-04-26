import csv
from scipy import sparse

import pandas as pd
import time

type_dict = {}
chunklist = []

db = pd.read_csv("finalSNPOrder.csv", chunksize=100)
cnt = 0
for i in db:
    cnt += 1
    start_time = time.time()
    chunklist.append(i)
    print("-------->",cnt)
    print("--- %s seconds ---" % (time.time() - start_time))
snp = pd.concat(chunklist)

print(snp)

snp = snp.drop(["Unnamed: 0"], axis=1)

column1 = snp[['name/ pos- ref- alt']]

column1 = column1.values.tolist()

snp = snp.drop(["name/ pos- ref- alt"], axis=1)

snp = snp.loc[:, snp.sum() > 0]

result = snp.values.tolist()

for i in range(0, len(result)):
    del result[i][0]

for j in range(0, len(result[0])):
    for i in range(0, len(result)):
        result[i][j] = int(result[i][j])

mtx = sparse.lil_matrix(result)

mtxcoo = mtx.tocoo()

sparse.save_npz("yourmatrix.npz", mtxcoo)

sparse = sparse.load_npz("yourmatrix.npz")

with open("column1.csv", "w") as f:  # newline="") as f:
    writer = csv.writer(f)
    writer.writerows(column1)

from scipy import sparse

sparse = sparse.load_npz("sparsetable.npz")
