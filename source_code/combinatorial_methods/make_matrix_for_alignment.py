import pandas as pd
import sys

def get_sequences_for_cluster(dataset, id_cluster):

	sequence_id = []

	for i in range(len(dataset)):
		if dataset['clusterID'][i] == id_cluster:
			sequence_id.append(dataset['sequence'][i])

	return sequence_id

dataset = pd.read_csv(sys.argv[1])
path_to_Data = sys.argv[2]

matrix_data = []

for i in range(len(dataset)):
	matrix_data.append([0 for x in range(len(dataset))])

list_clusters = list(set(dataset['clusterID']))

for cluster in list_clusters:

	list_sequences = get_sequences_for_cluster(dataset, cluster)
	for element1 in list_sequences:
		for element2 in list_sequences:
			matrix_data[element1-1][element2-1]+=1

header = ["P_"+str(i+1) for i in range(len(matrix_data))]
dataset_export = pd.DataFrame(matrix_data, columns=header)
dataset_export.to_csv(path_to_Data+"join_matrix_data.csv", index=False)