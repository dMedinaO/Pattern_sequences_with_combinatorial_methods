import sys
import os

python_script = "make_matrix_based_exploring.py"

path_data = sys.argv[1]

list_path = ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]

for path in list_path:

	command = "python3 %s %s%s/categories_exploring.csv %s%s/" % (python_script, path_data, path, path_data, path)
	print(command)
	os.system(command)
	