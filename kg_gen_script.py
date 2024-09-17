import pandas as pd
import numpy as np
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('start_ind')
parser.add_argument('end_ind')
parser.add_argument('batch_num')
parser.add_argument('-n', action='store_true')
args = parser.parse_args()


adj_nodes = pd.read_csv("nodes.csv")
adj_nodes = adj_nodes.drop(['node_id', 'node_source', 'node_index'], axis=1)
with open("adj_list.pickle", "rb") as f:
    adj_list = pickle.load(f)


def gen_subgraph(start_node, end_node):
    node_vec = np.full((len(adj_nodes), 3), [-1, -1, -1])   # [ start_dist, end_dist, index in node_set]
    q = [start_node]        # BFT Queue
    node_vec[start_node][0] = 0
    node_vec[end_node][1] = 0
    for i in range(2):
        temp_q = []
        for k in q:
            for j in adj_list[k]:
                for l in j:
                    if node_vec[abs(l)][0] == -1:
                        node_vec[abs(l)][0] = i+1
                    temp_q.append(abs(l))
        q.clear()
        q.extend(temp_q)
    q.clear()
    q.append(end_node)
    for i in range(2):
        temp_q = []
        for k in q:
            for j in adj_list[k]:
                for l in j:
                    if node_vec[abs(l)][1] == -1:
                        node_vec[abs(l)][1] = i+1
                    temp_q.append(abs(l))
        q.clear()
        q.extend(temp_q)
    node_set = set()
    for i in range(len(node_vec)):
        if (node_vec[i][0] != -1) and (node_vec[i][1] != -1) and (node_vec[i][0] + node_vec[i][1] <=3):
            node_set.add(i)
    node_set = list(node_set)
    for i in range(len(node_set)):
        node_vec[node_set[i]][2] = i
    n_si = node_vec[start_node][2]
    n_ei = node_vec[end_node][2]
    matrix = np.zeros((len(node_set), len(node_set)), dtype=np.int8)
    #matrix = np.zeros((4000, 4000), dtype=np.int8)
    for i in range(len(node_set)):
        if node_vec[node_set[i]][0] == 1:
            if adj_nodes['node_type'][node_set[i]] == 'phenotype':
                for k in adj_list[start_node][2]:
                    if -k == node_set[i]:
                        matrix[n_si][i] = -1
                        matrix[i][n_si] = -1
                    elif k == node_set[i]:
                        matrix[n_si][i] = 1
                        matrix[i][n_si] = 1
            elif adj_nodes['node_type'][node_set[i]] == 'drug':
                for k in adj_list[start_node][1]:
                    if -k == node_set[i]:
                        matrix[n_si][i] = -1
                        matrix[i][n_si] = -1
                    elif k == node_set[i]:
                        matrix[n_si][i] = 1
                        matrix[i][n_si] = 1
            else:
                matrix[n_si][i] = 1
                matrix[i][n_si] = 1
            for j in adj_list[node_set[i]]:
                for k in j:
                    if node_vec[abs(k)][2] != -1:
                        matrix[i][node_vec[abs(k)][2]] = k/abs(k)
                        matrix[node_vec[abs(k)][2]][i] = k/abs(k)
        if node_vec[node_set[i]][1] == 1:
            if adj_nodes['node_type'][node_set[i]] == 'disease':
                for k in adj_list[start_node][3]:
                    if -k == node_set[i]:
                        matrix[n_ei][i] = -1
                        matrix[i][n_ei] = -1
                    elif k == node_set[i]:
                        matrix[n_ei][i] = 1
                        matrix[i][n_ei] = 1
            else:
                matrix[n_ei][i] = 1
                matrix[i][n_ei] = 1
            for j in adj_list[node_set[i]]:
                for k in j:
                    if node_vec[abs(k)][2] != -1:
                        matrix[i][node_vec[abs(k)][2]] = k/abs(k)
                        matrix[node_vec[abs(k)][2]][i] = k/abs(k)
    matrix[n_si][n_ei] = 0
    matrix[n_ei][n_si] = 0
    labels = np.zeros(len(node_set), dtype=np.int8)
    for i in range(len(node_set)):
        if i == n_si or i == n_ei:
            labels[i] = 0
            continue
        if node_vec[node_set[i]][0] == 1:
            if node_vec[node_set[i]][1] == 1:
                labels[i] = 1
            elif node_vec[node_set[i]][1] == 2:
                labels[i] = 2
        elif node_vec[node_set[i]][1] == 1:
            #if node_vec[node_set[i]][0] == 1:
                #labels[i] = 1
            if node_vec[node_set[i]][0] == 2:
                labels[i] = 3
    for i in range(len(matrix)):
        matrix[i][i] = 1
    return matrix, [adj_nodes['node_type'][i] for i in node_set], n_si, n_ei, labels


table_npz = None
pref = "pos"
if args.n:
    table_npz = np.load('neg_table.npy.npz')
    pref = "neg"
else:
    table_npz = np.load('pos_table.npy.npz')
table = table_npz.f.arr_0
table_npz.close()
batch = []
nodes_ind = {"gene/protein": 0, "drug": 1, "effect/phenotype": 2, "disease": 3, "biological_process": 4, "molecular_function": 5, "cellular_component": 6, "exposure": 7, "pathway": 8, "anatomy": 9}
# attr_vec format -> [type|start or end|structural label]
for i in range(int(args.start_ind), int(args.end_ind)):
    sg, v, s, e, labels = gen_subgraph(table[i][0], table[i][1])
    attr_mat = np.zeros((len(labels), 16), dtype=np.int8)
    for j in range(len(attr_mat)):
        if j < len(v):
            attr_mat[j][nodes_ind[v[j]]] = 1    # Attr concat
            attr_mat[j][12+labels[j]] = 1   # Label concat
    attr_mat[s][10] = 1     # Start node encode
    attr_mat[e][11] = 1     # End node encode
    batch.append([table[i][0], table[i][1], sg, attr_mat])
np.savez_compressed(f"{pref}_batch_{args.batch_num}", np.array(batch, dtype=object))
print(f"Done processing batch {args.batch_num}\n")
exit()
