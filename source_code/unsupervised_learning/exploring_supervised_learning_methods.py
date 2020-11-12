import pandas as pd
import sys
from sklearn import preprocessing
import processClustering
import evaluationClustering

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

#take all elements in dataset based on points in encoding process
matrix_data = []

headers = [key for key in dataset.keys() if key[0] == "P"]

for i in range(len(dataset)):
	row = [dataset[key][i] for key in headers]
	matrix_data.append(row)

#scaling dataset
min_max_scaler = preprocessing.MinMaxScaler()
dataset_process = min_max_scaler.fit_transform(matrix_data)

matrix_response = []
dataset_categories = pd.DataFrame()
dataset_categories['id_sequence_by_algorithm'] = dataset['id_sequence_by_algorithm']

clustering_data = processClustering.aplicateClustering(dataset_process)

#k-means
for i in range(2, 100):	
	if clustering_data.aplicateKMeans(i) == 0:
		row = ["K-means", i]
		print("K-means ", i)
		eval_clustering = evaluationClustering.evaluationClustering(dataset_process, clustering_data.labels)
		row.append(eval_clustering.calinski)
		row.append(eval_clustering.siluetas)
		matrix_response.append(row)
		key = "K-means-%d" % i
		dataset_categories[key] = clustering_data.labels
		

#birch

for i in range(2, 100):	
	if clustering_data.aplicateBirch(i) == 0:
		row = ["Birch", i]
		print("Birch ", i)
		eval_clustering = evaluationClustering.evaluationClustering(dataset_process, clustering_data.labels)
		row.append(eval_clustering.calinski)
		row.append(eval_clustering.siluetas)
		matrix_response.append(row)
		print(row)
		key = "Birch-means-%d" % i
		dataset_categories[key] = clustering_data.labels
		

#agglomerative clustering
for linkage in ['ward', 'complete', 'average', 'single']:
	for affinity in ['euclidean', 'l1', 'l2', 'manhattan', 'cosine', 'precomputed']:
		for i in range(2, 100):	
			if clustering_data.aplicateAlgomerativeClustering(linkage, affinity, i) == 0:
				params = "%s-%s-%d" % (linkage, affinity, i)
				print("Agglomerative ", params)
				row = ["Agglomerative", params]
				eval_clustering = evaluationClustering.evaluationClustering(dataset_process, clustering_data.labels)
				row.append(eval_clustering.calinski)
				row.append(eval_clustering.siluetas)
				matrix_response.append(row)
				key = "Agglomerative-%s-%s-%d" % (linkage, affinity, i)
				dataset_categories[key] = clustering_data.labels
				

#Affinity Propagation
if clustering_data.aplicateAffinityPropagation() == 0:
	row = ["Affinity-Propagation", "Default"]
	print("Affinity-Propagation")
	eval_clustering = evaluationClustering.evaluationClustering(dataset_process, clustering_data.labels)
	row.append(eval_clustering.calinski)
	row.append(eval_clustering.siluetas)
	matrix_response.append(row)
	dataset_categories["Affinity-Propagation"] = clustering_data.labels

#Mean Shift
if clustering_data.aplicateMeanShift() == 0:
	row = ["Mean-Shift", "Default"]
	print("Mean-Shift")
	eval_clustering = evaluationClustering.evaluationClustering(dataset_process, clustering_data.labels)
	row.append(eval_clustering.calinski)
	row.append(eval_clustering.siluetas)
	matrix_response.append(row)
	dataset_categories["Mean-Shift"] = clustering_data.labels

if clustering_data.aplicateDBSCAN() == 0:
	row = ["DBSCAN", "Default"]
	print("DBSCAN")
	eval_clustering = evaluationClustering.evaluationClustering(dataset_process, clustering_data.labels)
	row.append(eval_clustering.calinski)
	row.append(eval_clustering.siluetas)
	matrix_response.append(row)
	dataset_categories["DBSCAN"] = clustering_data.labels

dataset_categories.to_csv(path_output+"categories_data.csv", index=False)

dataset_export = pd.DataFrame(matrix_response, columns=['Algorithm', 'Params', 'calinski', 'siluetas'])
dataset_export.to_csv(path_output+"summary_report.csv", index=False)