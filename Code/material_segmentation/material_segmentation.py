import xml.etree.ElementTree as ET
import sys, getopt
import datetime

def main(argv):
	materialsFile = "coeff_diff.xml"
	directionsFile = "directions.xml"
	inputFile = "inputMaterials.txt"
	try:
		opts, args = getopt.getopt(argv,"m:d:i:",["materials=","directions=","input="])
	except getopt.GetoptError:
		print('material_segmentation.py -m coeff_diff.xml -d directions.xml -i inputMaterials.txt')
		sys.exit(2)
	for opt, arg in opts: #read and assign command parameters if used
		if opt in ("-m", "--materials"):
			materialsFile = arg
		elif opt in ("-d", "--directions"):
			directionsFile = arg
		elif opt in ("-i", "--input"):
			inputFile = arg
	
	now = datetime.datetime.now()
	directionTree = ET.parse(directionsFile) #read sun direction file and save it as the old version
	directionTree.write(directionsFile.split(".")[0]+"_"+now.strftime("%Y%m%d_%H%M")+".xml")
	directionRoot = directionTree.getroot()
	sunDirection = directionRoot[0][0]
	sunDirection.set("sunViewingZenithAngle","0") #change sun direction to avoid shadows
	directionTree.write(directionsFile) #save directions file
	
	
	inputText = open(inputFile, "r")
	lines=[]
	for line in inputText: #open materials text file, and save contents to array
		lines.append(line)
	
	materialTree = ET.parse(materialsFile) #read materials file and save it as the old version
	materialTree.write(materialsFile.split(".")[0]+"_"+now.strftime("%Y%m%d_%H%M")+".xml")
	materialRoot = materialTree.getroot()
	materials = materialRoot[0][0] #get materials section of the xml file
	
	index = 0
	for material in materials.findall("LambertianMulti"):#for each material in the simulation
		material.set("databaseName","Lambertian_label.db") #change the material database file
		fileValue = lines[index].replace("\n","") if index < len(lines) else " Red"#select the color from the file, if the file is long enough. Defaults to color red
		if fileValue == "Red" or fileValue == "red" or fileValue == "0": #set the color of the material according to the value of the text file
			material.set("ModelName", "Red")
		elif fileValue == "Green" or fileValue == "green" or fileValue == "1":
			material.set("ModelName", "Green")
		elif fileValue == "Blue" or fileValue == "blue" or fileValue == "2":
			material.set("ModelName", "Blue")
		elif fileValue == "Yellow" or fileValue == "yellow" or fileValue == "3":
			material.set("ModelName", "Yellow")
		elif fileValue == "Purple" or fileValue == "purple" or fileValue == "4":
			material.set("ModelName", "Purple")
		elif fileValue == "Cyan" or fileValue == "cyan" or fileValue == "5":
			material.set("ModelName", "Cyan")
		else:
			material.set("ModelName", "Red")
			
		index += 1
	
	inputText.close()
	materialTree.write(materialsFile) #write xml file
		
if __name__ == "__main__":
	main(sys.argv[1:])
 