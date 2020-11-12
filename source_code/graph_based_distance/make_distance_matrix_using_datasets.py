import pandas as pd
import sys
from Bio import SeqIO
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt

def make_histogram_for_distance(data_distance, name_output, name_distance):

	plt.clf()

	# An "interface" to matplotlib.axes.Axes.hist() method
	n, bins, patches = plt.hist(x=data_distance, bins='auto', color='#0504aa',
	                            alpha=0.7, rwidth=0.85)
	plt.grid(axis='y', alpha=0.75)
	plt.xlabel('Value')
	plt.ylabel('Frequency')
	plt.title(name_distance)	
	maxfreq = n.max()
	# Set a clean upper y-axis limit.
	plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)

	plt.savefig(name_output)


def get_distance_vectors (dataset, index1, index2):

	vector1 = dataset[index1]
	vector2 = dataset[index2]

	mahalonobis_distance = distance.cityblock(vector1, vector2)
	cosine_distance = distance.cosine(vector1, vector2)
	correlation_distance = distance.correlation(vector1, vector2)

	return mahalonobis_distance, cosine_distance, correlation_distance

dataset_input = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

matrix_data = []

headers = [key for key in dataset_input.keys() if key[0] == "P"]

for i in range(len(dataset_input)):
	row = [dataset_input[key][i] for key in headers]
	matrix_data.append(row)

print("Get matrix distance")

vector_distance_cosine = []
vector_distance_mahalonobis = []
vector_distance_correlation = []
vector_combinations = []

for i in range(len(dataset_input)):
	for j in range(len(dataset_input)):
		
		if i != j:

			combination1 = str(dataset_input['id_sequence_by_algorithm'][i])+"-"+ str(dataset_input['id_sequence_by_algorithm'][j])
			combination2 = str(dataset_input['id_sequence_by_algorithm'][j])+"-"+ str(dataset_input['id_sequence_by_algorithm'][i])			
						
			#note, Always I need to work with combination 1
			if combination1 not in vector_combinations and combination2 not in vector_combinations:
				print(combination1)
				vector_combinations.append(combination1)

				mahalonobis_distance, cosine_distance, correlation_distance = get_distance_vectors (matrix_data, i, j)
				vector_distance_cosine.append(cosine_distance)
				vector_distance_correlation.append(correlation_distance)
				vector_distance_mahalonobis.append(mahalonobis_distance)

print("Make histogram")
#get histogram for distances
make_histogram_for_distance(vector_distance_cosine, path_output+"cosine_distance.png", "Cosine distance")
make_histogram_for_distance(vector_distance_mahalonobis, path_output+"mahalonobis_distance.png", "Mahalonobis distance")
make_histogram_for_distance(vector_distance_correlation, path_output+"correlation_distance.png", "Correlation distance")

print("Export data to csv file")

#make dataset and export elements
dataset = pd.DataFrame()
dataset['combinations'] = vector_combinations
dataset['mahalonobis_distance'] = vector_distance_mahalonobis
dataset['cosine_distance'] = vector_distance_cosine
dataset['correlation_distance'] = vector_distance_correlation

dataset.to_csv(path_output+"distance_sequences.csv", index=False)