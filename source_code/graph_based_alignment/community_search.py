import pandas as pd
import sys
import numpy as np
import networkx as nx
import community as community_louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt

def make_histogram_distribution(list_data, output_data):

	mean_data = np.mean(list_data)
	iq1 = np.quantile(list_data, .25)
	iq3 = np.quantile(list_data, .75)

	plt.clf()

	# An "interface" to matplotlib.axes.Axes.hist() method
	n, bins, patches = plt.hist(x=list_data, bins='auto', color='#0504aa',
	                            alpha=0.7, rwidth=0.85)
	plt.grid(axis='y', alpha=0.75)
	plt.xlabel('Value')
	plt.ylabel('Frequency')
	plt.title('Score Histogram')	
	maxfreq = n.max()
	# Set a clean upper y-axis limit.
	plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)

	min_ylim, max_ylim = plt.ylim()

	plt.axvline(mean_data, color='k', linestyle='dashed', linewidth=2)
	plt.text(mean_data*1.1, max_ylim*0.9, 'Mean: {:.2f}'.format(mean_data))
	plt.axvline(iq1, color='r', linestyle='dashed', linewidth=2)
	plt.text(iq1*1.1, max_ylim*0.5, 'Q1: {:.2f}'.format(iq1))
	plt.axvline(iq3, color='b', linestyle='dashed', linewidth=2)
	plt.text(iq3*1.1, max_ylim*0.1, 'Q3: {:.2f}'.format(iq3))
	plt.savefig(output_data)

def get_quartiles(list_data):

	response = []

	for quartil in [0.25, 0.75]:
		response.append(np.quantile(list_data, quartil))

	return response

def get_outlier(quartile_list):

	iqr = quartile_list[1] - quartile_list[0]
	lower_bound = quartile_list[0] -(.5 * iqr) 
	upper_bound = quartile_list[1] +(.5 * iqr)

	return lower_bound, upper_bound

def get_outlier_based_distribution(list_data):

	mean_data = np.mean(list_data)
	std_data = np.std(list_data)

	upper_bound = mean_data+std_data
	return std_data

def create_graph_structure(dataset, threshold_upper, list_sequences):

	print("Process graph, ")
	graph_data = nx.Graph()

	#add nodes
	for sequence in list_sequences:
		graph_data.add_node(sequence)

	#add edges based on threshold
	for i in range(len(dataset)):

		data = dataset['sequences'][i].split("-")

		if dataset['score'][i] >threshold_upper:			
			graph_data.add_edge(data[0], data[1], weigth=dataset['score'][i])

	return graph_data

def community_research(graph_data, data_output):

	plt.clf()
	partition = community_louvain.best_partition(graph_data, resolution=1.0, weight='weight')
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


	# draw the graph
	pos = nx.spring_layout(graph_data)
	# color the nodes according to their partition
	cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
	nx.draw_networkx_nodes(graph_data, pos, partition.keys(), node_size=40,
	                       cmap=cmap, node_color=list(partition.values()))
	nx.draw_networkx_edges(graph_data, pos, alpha=0.5)	
	plt.savefig("testing_graph_figure.png")

def girvan_newman(graph):
	
	# find number of connected components
	sg = nx.connected_components(graph)
	sg_count = nx.number_connected_components(graph)

	while(sg_count == 1):
		graph.remove_edge(edge_to_remove(graph)[0], edge_to_remove(graph)[1])
		sg = nx.connected_components(graph)
		sg_count = nx.number_connected_components(graph)

	return sg

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

#get percentile by distribution
quartil_dist = get_quartiles(dataset['score'])

make_histogram_distribution(dataset['score'], path_output+"histogram_score.png")

#get threshold for each type of distance
threshold_lower, threshold_upper = get_outlier(quartil_dist)

#threshold_upper_based_distribution = get_outlier_based_distribution(dataset['score'])

#get list sequences
array_sequences = []

for combination in dataset['sequences']:
	data = combination.split("-")
	for element in data:
		array_sequences.append(element)

array_sequences = list(set(array_sequences))

#create grahp structures
graph_FFT = create_graph_structure(dataset, threshold_upper, array_sequences)

#apply clustering research
print("Get community in alignment method distance")
#community_research(graph_FFT, path_output+"clustering_distance.csv")

c = girvan_newman(graph_FFT.copy())

# find the nodes forming the communities
node_groups = []

for i in c:
	node_groups.append(list(i))

print(len(node_groups))
'''
# plot the communities
color_map = []
for node in graph_FFT:
    if node in node_groups[0]:
        color_map.append('blue')
    else: 
        color_map.append('green')  

nx.draw(graph_FFT, node_color=color_map, with_labels=True)
plt.show()
'''