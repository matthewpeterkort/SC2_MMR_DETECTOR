import pytesseract
import cv2
import pygetwindow
import pyautogui
import numpy as np
import time
import re

# only take 4 digit numbers
# if break read values from the file and start from there

# construct the argument parser and parse the arguments
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

count=0
FiveKcount=0
Unknowncount=0
imagenumber=0

with open('4KCounter.txt') as f:
    lines = f.readlines()
    next_count =lines[0]
    count = int(next_count[6])

with open('5KCounter.txt') as f:
    lines = f.readlines()
    next_count =lines[0]
    FiveKcount = int(next_count[6])
  
print("COUNT",count,FiveKcount)
while(1):
	
	#y= pygetwindow.getWindowsWithTitle('StarCraft II')[0]
	#y.activate()
	#print(y)
	
	img = pyautogui.screenshot()
	img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
	cv2.imwrite("in_memory_to_disk"+str(imagenumber)+".png", img)
	image = cv2.imread("in_memory_to_disk"+str(imagenumber)+".png")
	#image = cv2.imread("example_image_two"+".png")
	imagenumber=imagenumber+1
	crop_img = image[465:490, 1400:1450]
	gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
	ret,thresh1 = cv2.threshold(gray,80,255,cv2.THRESH_BINARY)
	#cv2.imshow("crop",image)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	text = pytesseract.image_to_string(thresh1,config='digits')
	crop_img_two = image[465:490, 470:515]
	gray_two = cv2.cvtColor(crop_img_two, cv2.COLOR_BGR2GRAY)
	ret,thresh2 = cv2.threshold(gray_two,80,255,cv2.THRESH_BINARY)


	#cv2.imshow("crop",thresh2)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()

	text_two = pytesseract.image_to_string(thresh2,config='digits')
	
	new_text_two= ""
	new_text= ""
	for m in text_two:
		if m.isdigit():
			new_text_two = new_text_two + m
	for n in text:
		if n.isdigit():
			new_text = new_text + n
	print(new_text,new_text_two)

	
	if ((not new_text.isdigit()) and (not new_text_two.isdigit())):
		print("we here")
		imagenumber=imagenumber-1

	elif(int(new_text) < 4000 or int(new_text_two) < 4000):
		print("we here 4 error")
		imagenumber=imagenumber-1
	
	else:
		if(int(new_text) < 5000 or int(new_text_two) < 5000 ):
			count=count+1
			replace_line('4KCounter.txt', 0, '4ks = '+str(count))
			time.sleep(30)
	
		elif(int(new_text) > 5000 and int(new_text_two) > 5000 ):
			FiveKcount=FiveKcount+1
			replace_line('5KCounter.txt', 0, '5ks = '+str(FiveKcount))
			time.sleep(30)
	
		else:
			Unknowncount=Unknowncount+1
			replace_line('unkown.txt', 0, 'Unranked/LeftLeague = '+str(Unknowncount))
			time.sleep(30)
		
		
	time.sleep(3)



