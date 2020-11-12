import pandas as pd
import sys

def get_element_by_groups(list_value, group_id):

	list_members_index=[]

	for i in range(len(list_value)):

		if list_value[i] == group_id:
			list_members_index.append(i)

	return list_members_index

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

matrix_pbb_data = []

index_sequences =["P_"+str(i+1) for i in range(len(dataset))]

for i in range(len(dataset)):
	matrix_pbb_data.append([0 for x in range(len(dataset))])

keys = [key for key in dataset.keys() if key != "id_sequence_by_algorithm"]

for key in keys:
	print("Process key: ", key)
	list_groups = list(set(dataset[key]))
	
	#get elements by group
	for group in list_groups:
		list_members_index = get_element_by_groups(dataset[key], group)

		#get ids based on index
		ids_sequences = [dataset['id_sequence_by_algorithm'][element] for element in list_members_index]		

		for element1 in ids_sequences:
			for element2 in ids_sequences:
				matrix_pbb_data[element1-1][element2-1]+=1

#export matrix to csv value
dataset_export = pd.DataFrame(matrix_pbb_data, columns=index_sequences)
dataset_export.to_csv(path_output+"matrix_data_counts.csv", index=False)