import torch, argparse, numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('batch_num')
args = parser.parse_args()

batch_dat = np.load(f'neg_batch_{args.batch_num}.npz', allow_pickle=True)
table = batch_dat.f.arr_0
edge_attrs = []
for entry in table:
    a = torch.tensor(entry[2]).to_sparse_coo()
    edge_atr = []
    for i in a.values():
        if i == 1:
            edge_atr.append([1, 0])
        else:
            edge_atr.append([0, 1])
    edge_attrs.append(np.array(edge_atr, dtype=np.int8))
np.savez_compressed(f"neg_edge_attr_{args.batch_num}.npz", np.array(edge_attrs, dtype=object))

#Positive batches
batch_dat = np.load(f'pos_batch_{args.batch_num}.npz', allow_pickle=True)
table = batch_dat.f.arr_0
edge_attrs = []
for entry in table:
    a = torch.tensor(entry[2]).to_sparse_coo()
    edge_atr = []
    for i in a.values():
        if i == 1:
            edge_atr.append([1, 0])
        else:
            edge_atr.append([0, 1])
    edge_attrs.append(np.array(edge_atr, dtype = np.int8))
np.savez_compressed(f"pos_edge_attr_{args.batch_num}.npz", np.array(edge_attrs, dtype=object))
