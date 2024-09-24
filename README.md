# MLGHPCE24DP

Datasets:
WN18: Use pip install dgl
OGBL-BioKG: Use pip install ogb
Cora: Can be imported from torch_geometric.datasets.Planetoid
PrimeKG: To generate training and testing data for PrimeKG, execute "python kg_multi_proc_table_gen.py". Keep all the files in the same directory.

Evaluation Experiments
Experiment: Recording the model performance across epochs, do the following:
Cora: Edit the file 'Planetoid\_bench.ipynb' by modifying line 1 of block 11 to adjust the number of epochs.
OGBL-BioKG: Edit the file 'bio\_kg\_bench.ipynb' by modifying line 1 of block 20 to adjust the number of epochs.
WN18: Edit the file 'WN18\_benchmark.ipynb' by modifying line 1 of block 11 to adjust the number of epochs.
PrimeKG: Edit the file 'GNN.ipynb' by modifying line 1 of block 7 to adjust the number of epochs.

Experiment: Recording model performance across the number of training samples, do the following:

OGBL-BioKG: Edit the file 'bio\_kg\_bench.ipynb' by modifying line 6 of block 19 to adjust the number of batches to train.
WN18: Edit the file 'WN18\_benchmark.ipynb' by modifying lines 6, 8 and 10 of block 6 to adjust the number of training samples in the trainer.
PrimeKG: Edit the file 'GNN.ipynb' by modifying line 3 of block 7 to adjust the number of batches to train.
