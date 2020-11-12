import pandas as pd
import sys

def get_sequences_for_cluster(dataset, id_cluster):

	sequence_id = []

	for i in range(len(dataset)):
		if dataset['clusterID'][i] == id_cluster:
			sequence_id.append(dataset['sequence'][i])

	return sequence_id

path_to_Data = sys.argv[1]

list_properties = ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]

array_datasets = []

for value in list_properties:
	dataset = pd.read_csv(path_to_Data+value+"/clustering_distance.csv")
	array_datasets.append(dataset)

#make matrix with 0 values
matrix_data = []

for i in range(len(array_datasets[0])):
	matrix_data.append([0 for x in range(len(array_datasets[0]))])


for dataset in array_datasets:

	list_id_clusters = list(set(dataset['clusterID']))

	#get sequences for each cluster
	for cluster in list_id_clusters:
		sequence_data = get_sequences_for_cluster(dataset, cluster)

		for element1 in sequence_data:
			for element2 in sequence_data:
				matrix_data[element1-1][element2-1]+=1

header = ["P_"+str(i+1) for i in range(len(array_datasets[0]))]
dataset_export = pd.DataFrame(matrix_data, columns=header)
dataset_export.to_csv(path_to_Data+"join_matrix_data.csv", index=False)