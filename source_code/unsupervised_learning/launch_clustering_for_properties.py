import os
import sys

properties = ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]

script = "exploring_supervised_learning_methods.py"

raw_path = sys.argv[1]
export_data = sys.argv[2]

for propertie_data in properties:
	command = "mkdir -p "+export_data+propertie_data
	print(command)
	os.system(command)

	command = "python3 %s %s%s/%s.csv %s%s/" %(script, raw_path, propertie_data, propertie_data, export_data, propertie_data)
	print(command)
	os.system(command)	
	