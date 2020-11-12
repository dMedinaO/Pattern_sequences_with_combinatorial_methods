import pandas as pd
import sys
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

command = "mkdir -p "+path_output+"alignment_graph_clustering"
print(command)
os.system(command)

path_output = path_output+"alignment_graph_clustering/"

combination_sequences = []

matrix_score = []
distance_matrix = []
rows_encoding = []

for i in range(len(dataset)):
	row_score_distance = []

	print("Process sequence: ", dataset['id_sequence_by_algorithm'][i])

	for j in range(len(dataset)):

		if i != j:
			
			#make alignment
			alignments = pairwise2.align.globalms(dataset['sequence'][i], dataset['sequence'][j], 2, -1, -.5, -.1, score_only=True)			
			row_score_distance.append(alignments)

			combination1 = str(dataset['id_sequence_by_algorithm'][i])+"-"+ str(dataset['id_sequence_by_algorithm'][j])
			combination2 = str(dataset['id_sequence_by_algorithm'][j])+"-"+ str(dataset['id_sequence_by_algorithm'][i])

			if combination1 not in rows_encoding and combination2 not in rows_encoding:
				rows_encoding.append(combination1)
				distance_matrix.append(alignments)
		else:
			row_score_distance.append(100)
	matrix_score.append(row_score_distance)

#export matrix data, create heatmap and export distance matrix
dataset_export = pd.DataFrame()
dataset_export['sequences'] = rows_encoding
dataset_export['score'] = distance_matrix

dataset_export.to_csv(path_output+"summary_score.csv", index=False)

# create heatmap
sns.heatmap(matrix_score, cmap="PiYG")
plt.savefig(path_output+"heatmap_score.svg")