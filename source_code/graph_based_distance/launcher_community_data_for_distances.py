import sys
import os

path_input = sys.argv[1]

list_directory = ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]

for data in list_directory:
	command = "python3 community_search.py %s%s/distance_sequences.csv %s%s/" % (path_input, data, path_input, data)
	os.system(command)

