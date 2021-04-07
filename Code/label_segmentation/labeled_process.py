from matplotlib import pyplot as plt
from skimage import io
import sys, getopt
import colorsys

colors=[[255,0,0],
		[0,255,0],
		[0,0,255],
		[255,255,0],
		[255,0,255],
		[0,255,255]
] #colors: Red, Green, Blue, Yellow, Purple, Cyan
hsvColors=[
		colorsys.rgb_to_hsv(1,0,0),
		colorsys.rgb_to_hsv(0,1,0),
		colorsys.rgb_to_hsv(0,0,1),
		colorsys.rgb_to_hsv(1,1,0),
		colorsys.rgb_to_hsv(1,0,1),
		colorsys.rgb_to_hsv(0,1,1)
] #colors: Red, Green, Blue, Yellow, Purple, Cyan

def colorDistance(hueA, hueB): #return euclidian distance between two colors in RGB space
	return abs(hueA-hueB)#math.sqrt((pixelA[0]-pixelB[0])**2+(pixelA[1]-pixelB[1])**2+(pixelA[2]-pixelB[2])**2)

def getNearestColor(pixel): #return the nearest defined color to the pixel color
	minDist=1
	minIndex=-1
	index=0
	hsvPixel = colorsys.rgb_to_hsv(pixel[0]/255,pixel[1]/255,pixel[2]/255)
	for color in hsvColors:
		distance = colorDistance(hsvPixel[0], color[0])

		#print(distance)
		#if distance < 30: #if the distance is small enough, there's no need to compare the rest of colors
		#	return color
		if distance < minDist: #check if distance is smaller than the last smallest distance, change values if true
			minDist=distance
			minIndex=index
		index+=1
	return colors[minIndex] #return color with the minimum distance

def Process(name):
	fileName=name
	baseImage = io.imread(fileName) #open image file
	for x in range(baseImage.shape[0]):
		for y in range(baseImage.shape[1]):
		#for all pixels in the image
		# if all the channels have a low value, to avoid defaulting to red, average the values with neighbors to avoid errors:
			if all(baseImage[x][y]<100) and x>0 and y>0 and x<baseImage.shape[0]-1 and y<baseImage.shape[1]-1:
				color = [0,0,0]
				color += baseImage[x][y]
				color += baseImage[x][y+1]
				color += baseImage[x][y-1]
				color += baseImage[x+1][y]
				color += baseImage[x+1][y+1]
				color += baseImage[x+1][y-1]
				color += baseImage[x-1][y]
				color += baseImage[x-1][y+1]
				color += baseImage[x-1][y-1]
				color = color / 9
				baseImage[x][y] = getNearestColor(color) #process the average color of neighbors
			#if it's bright, or a corner of the image, process the color of the pixel
			else:
				baseImage[x][y] = getNearestColor(baseImage[x][y])
	plt.imsave(name, baseImage)#save image

def main(argv):
	inputFile = ""
	try:
		opts, args = getopt.getopt(argv,"i:",["input="])
	except getopt.GetoptError:
		print('labeled_process.py -i inputImage.png')
		sys.exit(2)
	for opt, arg in opts: #read and assign image file
		if opt in ("-i", "--input"):
			inputFile = arg
	Process(inputFile) #process the image file

if __name__ == "__main__":
	main(sys.argv[1:])