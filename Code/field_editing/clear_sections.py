from skimage import io
import os
import sys, getopt
import datetime


def Process(fieldFile, imageFile):
	now = datetime.datetime.now()
	newName = fieldFile.split(".")[0]+"_"+now.strftime("%Y%m%d_%H%M")+".txt"
	os.rename(fieldFile,newName)#rename current field file to have a backup version
	outputText = open(fieldFile,"w") #create the field file with old name
	oldText = open(newName) #open old field file
	outputText.write("complete transformation\n")

	image = io.imread(imageFile, as_gray="true")
	firstLine = True
	for item in oldText: 
		if not firstLine: #for each line of the field text file that has valid information
			itemData = item.split(" ")
			x = round(float(itemData[1])) #get the corresponding x and y coordinates of the field's item
			y = round(float(itemData[2]))
			if image[x][y] == 0: #if the coordinates correspond to a black part of the map, save that object, writing it to the new file
				outputText.write(item)
		firstLine = False
	outputText.close()
	oldText.close()
def ProcessOutput(fieldFile, imageFile, outputFile):
	#now = datetime.datetime.now()
	#newName = fieldFile.split(".")[0]+"_"+now.strftime("%Y%m%d_%H%M")+".txt"
	#os.rename(fieldFile,newName)#rename current field file to have a backup version
	outputText = open(outputFile,"w") #create the field file with old name
	oldText = open(fieldFile) #open old field file
	outputText.write("complete transformation\n")

	image = io.imread(imageFile, as_gray="true")
	firstLine = True
	for item in oldText: 
		if not firstLine: #for each line of the field text file that has valid information
			itemData = item.split(" ")
			x = round(float(itemData[1])) #get the corresponding x and y coordinates of the field's item
			y = round(float(itemData[2]))
			if x < image.shape[0] and y < image.shape[1]:
				if image[x][y] <= 0.25: #if the coordinates correspond to a black part of the map, save that object, writing it to the new file
					outputText.write(item)
		firstLine = False
	outputText.close()
	oldText.close()


def main(argv):
	fieldFile = "field.txt"
	fieldImage = "field.png"
	outputFile = ""
	try:
		opts, args = getopt.getopt(argv,"f:i:o:",["field=","image=","output="])
	except getopt.GetoptError:
		print('clear_sections.py -f field.txt -i image.png')
		sys.exit(2)
	for opt, arg in opts: #check for command parameters, and assign them if used
		if opt in ("-f", "--field"):
			fieldFile=arg
		elif opt in ("-i", "--image"):
			fieldImage=arg
		elif opt in ("-o", "--output"):
			outputFile=arg
	if outputFile =="":
		print("NOT KILLING")
		Process(fieldFile, fieldImage) #delete items from field file according to image map
	else:
		ProcessOutput(fieldFile, fieldImage, outputFile)
if __name__ == "__main__":
   main(sys.argv[1:])
   