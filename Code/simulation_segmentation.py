import sys, getopt
import os

def main(argv):
	folder = ""
	output = "OutputImage.png"
	inputmaterials="inputMaterials.txt"
	try:
		opts, args = getopt.getopt(argv,"s:o:i:",["simulation=","output=","inputmaterials="])
	except getopt.GetoptError:
		print('simulation_segmentation.py -s SimulationFolderPath -o OutputImage.png -i inputMaterials.txt')
		sys.exit(2)
	for opt, arg in opts: #read and assign command parameters
		if opt in ("-s", "--simulation"):
			folder = arg
		elif opt in ("-o", "--output"):
			output = arg
		elif opt in ("-i", "--inputmaterials"):
			inputmaterials = arg
	
	outputPath = folder+"\\output" #general output folder of the simulation
	print("Setting up Simulation "+folder.split("\\")[-1]) #printing process settings
	print("Folder: "+folder)
	print("Materials settings: " + inputmaterials)
	
	print("Setting up lighting and materials...") #adjust lighting and materials files
	os.system("python material_segmentation/material_segmentation.py -d "+folder+"/input/directions.xml -m "+folder+"/input/coeff_diff.xml -i "+inputmaterials)
	print("Lighting and materials adjusted.")

	print("Setting up camera...")
	os.system("python band_setting/band_setting.py -f "+folder+" -i band_setting/dart_camera_RGB.txt")
	print("Camera adjusted.")

	dartMainFolder = "\\".join(folder.split('\\')[:-3])
	dartToolFolder = dartMainFolder+"\\tools\\windows\\" #select dart's tools folder
	print("Executing DART...") #execute dart to render simulation with new materials
	os.system(dartToolFolder+"dart-full.bat "+folder.split("\\")[-1])# "" simulation_name="+folder.split("\\")[-1]
	
	print("\nCompositing images...")
	bandFolders = [f.path for f in os.scandir(outputPath) if f.is_dir()][:3]
	for i in range(3):#get each of the rendered images' path
		bandFolders[i] = '"'+bandFolders[i]+"\\BRF\\ITERX\\IMAGES_DART\\ima01_VZ=000_0_VA=000_0.mp#"+'"'
	R = bandFolders[2]
	G = bandFolders[1]
	B = bandFolders[0]
	os.system(dartToolFolder+"dart-colorComposite.bat "+R+" "+G+" "+B+" "+output)#execute color composition
	print("Color image composited.")
	
	print("Post processing composite labeled image...")
	os.system("python label_segmentation/labeled_process.py -i "+output)#post process image to get pallette colors, true to labels
	print("Done.")

if __name__ == "__main__":
	main(sys.argv[1:])