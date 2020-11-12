import os
import sys

properties = ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]
command = "time_series_clustering.py"

path_input = sys.argv[1]
path_output = sys.argv[2]

for value in properties:
	
	command_create_path = "mkdir -p "+path_output+value
	print(command_create_path)
	os.system(command_create_path)

	command_exec = "python3 %s %s%s/%s.csv %s%s/" % (command, path_input, value, value, path_output, value)	
	print(command_exec)
	os.system(command_exec)
		