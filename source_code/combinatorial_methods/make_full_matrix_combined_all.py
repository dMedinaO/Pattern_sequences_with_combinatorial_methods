import pandas as pd
import sys

path_data = sys.argv[1]

list_paths = ["alignment_graph_clustering", "digital_signal_processing", "graph_clustering/digital_signal_processing", "graph_clustering/physicochemical_properties", "graph_clustering/embedding", "unsupervised_learning"]

array_matrix_combined = []

for element in list_paths:
	print("Process ", element)
	dataset = pd.read_csv(path_data+element+"/join_matrix_data.csv")

	matrix_data = []
	for i in range(len(dataset)):
		row = []
		for key in dataset.keys():
			row.append(dataset[key][i])

		matrix_data.append(row)

	array_matrix_combined.append(matrix_data)

matrix_data_results = []

for i in range(len(array_matrix_combined[0])):
	matrix_data_results.append([0 for x in range(len(array_matrix_combined[0]))])

index=1
for matrix in array_matrix_combined:
	print("Process index", index)
	for i in range(len(matrix)):
		for j in range(len(matrix)):
			matrix_data_results[i][j]+=matrix[i][j]
	index+=1
	
header = ["P_"+str(i+1) for i in range(len(matrix_data_results))]
dataset_export = pd.DataFrame(matrix_data_results, columns=header)

dataset_export.to_csv(path_data+"full_combinated_data.csv", index=False)
