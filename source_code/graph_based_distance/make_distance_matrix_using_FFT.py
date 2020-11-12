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

#auxiliar function, rest points in vector
def rest_points_vector(x1, x2):

    response = []
    for i in range(len(x1)):#x1 es el menor rango
        value = x1[i]-x2[i]
        response.append(value)
    return response

#auxiliar function, get sum values in absolute form of difference between vectors
def getSumDifference(vector1, vector2):

    vector_rest = []
    for i in range(len(vector1)):
        result = abs(vector1[i]-vector2[i])
        vector_rest.append(result)
    return sum(vector_rest)

#calculate distance values vector1=x vector2=Y
def estimated_distance(vector1, vector2, alpha, order):

    n=1
    ds=0

    for i in range(order+1):
        vector = vector1+vector2
        max_data = float(max(vector))
        min_data = float(min(vector))
        a_i = alpha[i]/(max_data-min_data)
        sum_vector = getSumDifference(vector1, vector2)
        ds = ds + (a_i*sum_vector)
        vector1 = rest_points_vector(vector1[1:], vector1)
        vector2 = rest_points_vector(vector2[1:], vector2)

    return ds

dataset_input = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

matrix_data = []

headers = [key for key in dataset_input.keys() if key[0] == "P"]

for i in range(len(dataset_input)):
	row = [dataset_input[key][i] for key in headers]
	matrix_data.append(row)

print("Get matrix distance")

vector_distance = []
vector_combinations = []

alpha = [1 for x in matrix_data[0]]

for i in range(len(dataset_input)):
	for j in range(len(dataset_input)):
		
		if i != j:

			combination1 = str(dataset_input['id_sequence_by_algorithm'][i])+"-"+ str(dataset_input['id_sequence_by_algorithm'][j])
			combination2 = str(dataset_input['id_sequence_by_algorithm'][j])+"-"+ str(dataset_input['id_sequence_by_algorithm'][i])			
						
			#note, Always I need to work with combination 1
			if combination1 not in vector_combinations and combination2 not in vector_combinations:
				print(combination1)
				vector_combinations.append(combination1)

				distance = estimated_distance(matrix_data[i], matrix_data[j], alpha,2)				
				vector_distance.append(distance)
				

print("Make histogram")
#get histogram for distances
make_histogram_for_distance(vector_distance, path_output+"distance_histogram.png", "Time Serie Distance")

print("Export data to csv file")

#make dataset and export elements
dataset = pd.DataFrame()
dataset['combinations'] = vector_combinations
dataset['distance'] = vector_distance

dataset.to_csv(path_output+"distance_sequences.csv", index=False)