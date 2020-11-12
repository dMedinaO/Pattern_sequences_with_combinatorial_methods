import pandas as pd
import sys

path_data = sys.argv[1]

list_properties = ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]

array_matrix = []

for value in list_properties:
	dataset = pd.read_csv(path_data+value+"/matrix_data_counts.csv")
	matrix_value = []
	for i in range(len(dataset)):
		row = []
		for key in dataset.keys():
			row.append(dataset[key][i])
		matrix_value.append(row)
	array_matrix.append(matrix_value)

matrix_data_results = []

for i in range(len(array_matrix[0])):
	matrix_data_results.append([0 for x in range(len(array_matrix[0]))])

index=1
for matrix in array_matrix:
	print("Process index", index)
	for i in range(len(matrix)):
		for j in range(len(matrix)):
			matrix_data_results[i][j]+=matrix[i][j]
	index+=1
	
header = ["P_"+str(i+1) for i in range(len(matrix_data_results))]
dataset_export = pd.DataFrame(matrix_data_results, columns=header)

dataset_export.to_csv(path_data+"join_matrix_data.csv", index=False)