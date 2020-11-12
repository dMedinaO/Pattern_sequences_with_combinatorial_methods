import pandas as pd
import sys
import os
from tslearn.clustering import KShape, TimeSeriesKMeans
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from sklearn import metrics

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

#take all elements in dataset based on points in encoding process
matrix_data = []

headers = [key for key in dataset.keys() if key[0] == "P"]

for i in range(len(dataset)):
	row = [dataset[key][i] for key in headers]
	matrix_data.append(row)


# For this method to operate properly, prior scaling is required
X_train = TimeSeriesScalerMeanVariance().fit_transform(matrix_data)

matrix_scaler = []

for row in X_train:
	row_values = []
	for element in row:
		row_values.append(element[0])
	matrix_scaler.append(row_values)

matrix_response = []

dataset_categories = pd.DataFrame()
dataset_categories['id_sequence_by_algorithm'] = dataset['id_sequence_by_algorithm']

for k in range(2, 50):
	
	try:	
		print("Process K: ", k)					
		# kShape clustering
		ks = KShape(n_clusters=k, verbose=True, random_state=0)
		y_pred = ks.fit_predict(matrix_scaler)	

		siluetas = metrics.silhouette_score(matrix_scaler, y_pred, metric='euclidean')
		calinski = metrics.calinski_harabasz_score(matrix_scaler, y_pred)
		davies_index = metrics.davies_bouldin_score(matrix_scaler, y_pred)
		description = "K-"+str(k)

		row_summary = ["KShape_clustering", description, siluetas, calinski, davies_index]

		matrix_response.append(row_summary)
		dataset_categories[description] = y_pred			

	except:
		pass

dataset_categories.to_csv(path_output+"categories_exploring.csv", index=False)
dataSummary = pd.DataFrame(matrix_response, columns=["Algorithm", "Hyperparams", "silhouette_score", "calinski_harabasz_score", "davies_bouldin_score"])
dataSummary.to_csv(path_output+"summary_report.csv", index=False)
