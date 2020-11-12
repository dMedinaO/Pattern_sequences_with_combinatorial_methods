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

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]
path_digitized = sys.argv[3]

length_data = [len(sequence) for sequence in dataset['sequence']]
make_histogram(length_data, path_output+"length_histogram.png", "Length of sequences")

#make figure of digital signal process mean by property

property_values = ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]

plt.clf()
fig, ax = plt.subplots(4, 2, sharex=True, sharey=False, tight_layout=True)

index=0

for i in range(4):
	for j in range(2):
		value = property_values[index]
		data_input = pd.read_csv(path_digitized+value+"/summary_spectras.csv")

		df = pd.DataFrame({'domain':data_input['domain'][30:], 'y_value':data_input['average_curve'][30:], 'y_value_IC_low':data_input['lower_interval_IC'][30:], 'y_value_IC_high':data_input['upper_interval_IC'][30:]})
		
		# multiple line plot
		ax[i][j].plot( 'domain', 'y_value', data=df, marker='', linewidth=1.5, label=value)
		#ax[i][j].plot( 'domain', 'y_value_IC_low', data=df, marker='', linewidth=1.5, label=value)
		#ax[i][j].plot( 'domain', 'y_value_IC_high', data=df, marker='', linewidth=1.5, label=value)
		bottom = np.min(df['y_value_IC_low'])
		top = np.max(df['y_value_IC_high'])
		#ax[i][j].set_ylim((bottom, top)) 
		index+=1
		#ax[i][j].legend()
		ax[i][j].title.set_text(value)

plt.savefig(path_output+"summary_spectras.png")

