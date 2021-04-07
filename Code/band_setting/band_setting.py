import xml.etree.ElementTree as ET
import sys, getopt

def main(argv):
	fileName = "phase.xml"
	outputFileName = "phaseOutput.xml"
	inputFile = "input.txt"
	deleteOld = True
	try:
		opts, args = getopt.getopt(argv,"f:i:od",["file=","input=","output=", "deleteOld"])
	except getopt.GetoptError:
		print('band_setting.py -f simulationFolder -i input.txt [-o output.xml -d]')
		sys.exit(2)
	for opt, arg in opts: #check for command parameters, and assign them if used
		if opt in ("-f", "--file"):
			fileName=arg+"\\input\\phase.xml"
			outputFileName=fileName
		elif opt in ("-i", "--input"):
			inputFile=arg
		elif opt in ("-o", "--output"):
			outputFileName=arg
		elif opt in ("-d", "--deleteOld"):
			deleteOld = False
			
	
	inputText = open(inputFile, "r") #open text file containing camera data
	tree = ET.parse(fileName) #open, parse, and get root of phase xml file containing camera values
	root = tree.getroot()
	spectralIntervals=root[0][2][2] #select the spectral intervals section of the xml file
	if deleteOld:
		for interval in spectralIntervals.findall("SpectralIntervalsProperties"): #delete old spectral bands if wanted
			spectralIntervals.remove(interval)
	
	index = 0
	for line in inputText: #for each line of the text file, create a new spectral interval properties xml section
		values = line.split(" ")
		deltaLambda = deltaLambda = values[1].replace("\n","") if len(values)>1 else 0
		meanLambda = values[0].replace("\n","") #read values from text line, and assign them to the xml properties
		interval = ET.SubElement(spectralIntervals,"SpectralIntervalsProperties")
		interval.set("bandNumber", str(index))
		interval.set("deltaLambda",str(deltaLambda))
		interval.set("meanLambda",str(meanLambda))
		interval.set("spectralDartMode",str(0))
		index += 1
	inputText.close()
	
	tree.write(outputFileName)#output the resulting xml file
		
if __name__ == "__main__":
   main(sys.argv[1:])