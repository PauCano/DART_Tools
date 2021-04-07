import os
import sys, getopt

def Process(fieldFile, n):
	newName = fieldFile.split(".")[0]+"_old.txt"
	os.rename(fieldFile,newName)#rename current field file to have a backup version
	outputText = open(fieldFile,"w") #create the field file with old name
	oldText = open(newName) #open old field file

	x = 0
	for item in oldText:
		if x >= n: #every n objects, save that object, writing it to the new file
			outputText.write(item)
			x = -1
		x += 1	
	outputText.close()
	oldText.close()

def main(argv):
	fieldFile = "field.txt"
	n=10
	try:
		opts, args = getopt.getopt(argv,"f:n:",["field=","n="])
	except getopt.GetoptError:
		print('clearSections.py -f field.txt -n 10')
		sys.exit(2)
	for opt, arg in opts: #check for command parameters, and assign them if used
		if opt in ("-f", "--field"):
			fieldFile=arg
		elif opt in ("-n", "--n"):
			n=int(arg)
	Process(fieldFile, n) #delete items from field file

if __name__ == "__main__":
   main(sys.argv[1:])