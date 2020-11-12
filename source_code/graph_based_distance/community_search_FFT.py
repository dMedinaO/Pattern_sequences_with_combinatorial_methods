import pandas as pd
import sys
import numpy as np
import networkx as nx
import community as community_louvain

def get_quartiles(list_data):

	response = []

	for quartil in [0.25, 0.75]:
		response.append(np.quantile(list_data, quartil))

	return response

def get_outlier(quartile_list):

	iqr = quartile_list[1] - quartile_list[0]
	lower_bound = quartile_list[0] -(1.5 * iqr) 
	upper_bound = quartile_list[1] +(1.5 * iqr)

	return lower_bound, upper_bound

def create_graph_structure(dataset, distance_type, threshold_lower, threshold_upper, list_sequences):

	print("Process graph, ", distance_type)
	graph_data = nx.Graph()

	#add nodes
	for sequence in list_sequences:
		graph_data.add_node(sequence)

	#add edges based on threshold
	for i in range(len(dataset)):

		data = dataset['combinations'][i].split("-")

		if dataset[distance_type][i] <=threshold_lower:			
			graph_data.add_edge(data[0], data[1], weigth=dataset[distance_type][i])

	return graph_data

def community_research(graph_data, data_output):

	partition = community_louvain.best_partition(graph_data)
	try:
		modularity_value= community_louvain.modularity(partition, graph_data)
		print(modularity_value)
	except:
		print("Error getting modularity")
		pass

	matrix_data = []

	for data in partition:
		row = [data, partition[data]]
		matrix_data.append(row)

	dataFrame = pd.DataFrame(matrix_data, columns=["sequence", "clusterID"])
	dataFrame.to_csv(data_output, index=False)

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

#get percentile by distribution
quartil_distance = get_quartiles(dataset['distance'])

#get threshold for each type of distance
threshold_lower, threshold_upper = get_outlier(quartil_distance)

#get list sequences
array_sequences = []

for combination in dataset['combinations']:
	data = combination.split("-")
	for element in data:
		array_sequences.append(element)

array_sequences = list(set(array_sequences))

#create grahp structures
graph_distance = create_graph_structure(dataset, 'distance', threshold_lower, threshold_upper, array_sequences)

#apply clustering research
print("Get community distance")
community_research(graph_distance, path_output+"clustering_distance.csv")
