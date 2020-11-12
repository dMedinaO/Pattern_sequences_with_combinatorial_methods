import sys
import os

list_propertyes = ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]

path_input = sys.argv[1]
path_output = sys.argv[2]

for value in list_propertyes:
	command = "mkdir -p "+path_output+value
	print(command)
	os.system(command)

	command = "python3 make_distance_matrix_using_datasets.py %s%s/%s.csv %s%s/" % (path_input, value, value, path_output, value)
	print(command)
	
	os.system(command)