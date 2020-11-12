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

		if distance_type == "correlation_distance":
			if dataset[distance_type][i] <=threshold_lower or dataset[distance_type][i] >=threshold_upper:
				graph_data.add_edge(data[0], data[1], weigth=dataset[distance_type][i])
		else:
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
quartil_dist_mahalonobis = get_quartiles(dataset['mahalonobis_distance'])
quartil_dist_cosine = get_quartiles(dataset['cosine_distance'])
quartil_dist_correlation = get_quartiles(dataset['correlation_distance'])

#get threshold for each type of distance
threshold_mahalonobis_lower, threshold_mahalonobis_upper = get_outlier(quartil_dist_mahalonobis)
threshold_cosine_lower, threshold_cosine_upper = get_outlier(quartil_dist_cosine)
threshold_correlation_lower, threshold_correlation_upper = get_outlier(quartil_dist_correlation)

#get list sequences
array_sequences = []

for combination in dataset['combinations']:
	data = combination.split("-")
	for element in data:
		array_sequences.append(element)

array_sequences = list(set(array_sequences))

#create grahp structures
graph_mahalonobis = create_graph_structure(dataset, 'mahalonobis_distance', threshold_mahalonobis_lower, threshold_mahalonobis_upper, array_sequences)
graph_cosine = create_graph_structure(dataset, 'cosine_distance', threshold_cosine_lower, threshold_cosine_upper, array_sequences)
graph_correlation = create_graph_structure(dataset, 'correlation_distance', threshold_correlation_lower, threshold_correlation_upper, array_sequences)

#apply clustering research
print("Get community in correlation distance")
community_research(graph_correlation, path_output+"clustering_correlation_distance.csv")
print("Get community in cosine distance")
community_research(graph_cosine, path_output+"clustering_cosine_distance.csv")
print("Get community in mahalonobis distance")
community_research(graph_mahalonobis, path_output+"clustering_mahalonobis_distance.csv")
