import subprocess

for field in range(1,11):
	print("FIELD: " + str(field))
	for dry in range(1,9):
		print("----Dry: " + str(dry))
		output=subprocess.check_output("python change_model_sections.py -f input/field_"+str(field)+".txt -i input/dry_"+str(dry)+".png -m 1 -o output/field_"+str(field)+"_"+str(dry)+".txt",shell=True)
		print(output)
		for dead in range(1,9):
			print("--------Dead: " + str(dead))
			if dead <= dry:
				output=subprocess.check_output("python clear_sections.py -f output/field_"+str(field)+"_"+str(dry)+".txt -i input/dead_"+str(dead)+".png -o output/field_"+str(field)+"_"+str(dry)+"_"+str(dead)+".txt",shell=True)
				print(output)
	