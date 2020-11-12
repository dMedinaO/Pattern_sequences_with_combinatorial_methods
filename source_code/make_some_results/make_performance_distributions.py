import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt

def make_histogram(data_values, name_output, title):

	plt.clf()

	# An "interface" to matplotlib.axes.Axes.hist() method
	n, bins, patches = plt.hist(x=data_values, bins='auto', color='C2',
	                            alpha=0.7, rwidth=0.85)
	plt.grid(axis='y', alpha=0.75)
	plt.xlabel('Value')
	plt.ylabel('Frequency')
	plt.title(title)	
	maxfreq = n.max()

	min_ylim, max_ylim = plt.ylim()
	mean_data = np.mean(data_values)
	iq1 = np.quantile(data_values, .25)
	iq3 = np.quantile(data_values, .75)

	plt.axvline(mean_data, color='k', linestyle='dashed', linewidth=2)
	plt.text(mean_data*1.1, max_ylim*0.9, 'Mean: {:.2f}'.format(mean_data))
	plt.axvline(iq1, color='r', linestyle='dashed', linewidth=2)
	plt.text(iq1*1.1, max_ylim*0.5, 'Q1: {:.2f}'.format(iq1))
	plt.axvline(iq3, color='b', linestyle='dashed', linewidth=2)
	plt.text(iq3*1.1, max_ylim*0.1, 'Q3: {:.2f}'.format(iq3))	

	plt.savefig(name_output)

path_to_data = sys.argv[1]
path_results = sys.argv[2]

list_path = ["alpha-structure_group", "betha-structure_group", "embedding", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]

array_data_siluetas = []
array_data_calinkski = []

for file in list_path:

	dataset = pd.read_csv(path_to_data+file+"/summary_report.csv")

	for i in range(len(dataset)):
		try:
			array_data_calinkski.append(float(dataset['calinski'][i]))
			array_data_siluetas.append(float(dataset['siluetas'][i]))
		except:
			pass

make_histogram(array_data_siluetas, path_results+"histogram_for_siluetas.png", "Silhouette Index")
make_histogram(array_data_calinkski, path_results+"histogram_for_calinski.png", "Calinski-Harabasz Index")
