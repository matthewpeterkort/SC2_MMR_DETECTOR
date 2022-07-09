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
  
while(1):
	
	img = pyautogui.screenshot()
	image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
	#cv2.imwrite("in_memory_to_disk"+str(imagenumber)+".png", image)
	#image = cv2.imread("in_memory_to_disk"+str(imagenumber)+".png")
	#image = cv2.imread("tester"+".png")
	#image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

	crop_img = image[465:490, 1400:1450]
	resized = cv2.resize(crop_img, (100,100), interpolation = cv2.INTER_CUBIC  )
	new = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	retOne,resized = cv2.threshold(new,80,255,cv2.THRESH_BINARY)


	cropt_img_partTwo = image[442:469, 1461:1669]
	resized_TWO_TWO= cv2.resize(cropt_img_partTwo,  (200,45), interpolation = cv2.INTER_CUBIC             )
	gray_two = cv2.cvtColor(resized_TWO_TWO, cv2.COLOR_BGR2GRAY)
	retTwo,resized_TWO = cv2.threshold(gray_two,66,255,cv2.THRESH_BINARY)


	crop_img_two = image[442:469, 251:459]
	resized_THREE_THREE = cv2.resize(crop_img_two,  (200,45), interpolation = cv2.INTER_NEAREST             )
	gray_three = cv2.cvtColor(resized_THREE_THREE, cv2.COLOR_BGR2GRAY)
	retThree,resized_THREE = cv2.threshold(gray_three,66,255,cv2.THRESH_BINARY)

	crop_img_two_parttwo = image[465:490, 470:520]
	resized_two_two = cv2.resize(crop_img_two_parttwo, (100,100), interpolation = cv2.INTER_LINEAR              )
	gray_two_parttwo = cv2.cvtColor(resized_two_two, cv2.COLOR_BGR2GRAY)
	retFour,resized_two_two = cv2.threshold(gray_two_parttwo,80,255,cv2.THRESH_BINARY)

	
	#cv2.imshow("nesks",resized)
	#cv2.imshow("crop_two",resized_TWO)
	#cv2.imshow("crop_four",resized_THREE)
	#cv2.imshow("Test_img.jpg",resized_two_two)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()

	Right_Num= pytesseract.image_to_string(resized,lang="eurostile",config='digits')
	Right_Word= pytesseract.image_to_string(resized_TWO, lang='eurostile', config='--psm 7')
	
	Left_Word= pytesseract.image_to_string(resized_THREE,lang="eurostile", config='--psm 7' )
	Left_Num= pytesseract.image_to_string(resized_two_two,lang="eurostile", config='digits')


	new_Right_Num = ""
	new_Left_Num = ""
	new_Right_Word=""
	new_Left_Word=""
	
	
	for m in Right_Num:
		if m.isdigit():
			new_Right_Num = new_Right_Num + m
	for n in Left_Num:
		if n.isdigit():
			new_Left_Num = new_Left_Num + n
	for o in Right_Word:
		if o.isalpha() or o.count("<") or o.count(">"):
			new_Right_Word = new_Right_Word + o
	for p in Left_Word:
		if p.isalpha() or p.count("<") or p.count(">"):
			new_Left_Word = new_Left_Word + p

	race_crop_left = image[445:481, 521:559]
	race_crop_right = image[445:481,1361:1399]
	right_terran= cv2.imread("right_terran.png")
	right_zerg= cv2.imread("right_zerg.png")
	right_protoss= cv2.imread("right_protoss.png")
	left_terran= cv2.imread("left_terran.png")
	left_zerg= cv2.imread("left_zerg.png")
	left_protoss= cv2.imread("left_protoss.png")
	
	
	print("LISTENING",new_Left_Word + Left_Num, new_Right_Word + Right_Num)
	x = new_Right_Word.count("L")
	y = new_Left_Word.count("L")
	#cv2.imshow("race_CROPRIGHT",race_crop_right)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	if (new_Right_Word == "INI" or new_Right_Word == "III" or new_Right_Word == "LLLLLLLLLLLL" or new_Right_Word == "LLLLLILILILL" or new_Right_Word == "LLLULLLILILLE" or new_Right_Word == "HII"
	or new_Right_Word == "LLL" or new_Right_Word == "LLLLLULLLLLL"or new_Right_Word == "LLU" or x >= 5 ):
	
		if(np.all((race_crop_right - right_terran) == 0)):
			print("WE HERE")
			replace_line('Current_Oponnent.txt', 0,  'Terran IIIIIIIII ' + str(new_Right_Num) )
		if(np.all((race_crop_right - right_zerg) == 0)):
			replace_line('Current_Oponnent.txt', 0,  'Zerg IIIIIIIII ' + str(new_Right_Num) )
			print("WE HERE")
		if(np.all((race_crop_right - right_protoss) == 0)):
			print("WE HERE")
			replace_line('Current_Oponnent.txt', 0,  'Protoss IIIIIIIII ' + str(new_Right_Num) )
	
	elif (new_Left_Word == "INI" or new_Left_Word == "III" or new_Left_Word == "LLLLLLLLLLLL" or new_Left_Word == "LLLLLILILILL" or new_Left_Word == "LLLULLLILILLE" or new_Left_Word == "HII"
	or new_Left_Word == "LLL" or new_Left_Word == "LLLLLULLLLLL"or new_Left_Word == "LLU" or y >= 5 ):
		if(np.all((race_crop_left - left_terran) == 0)):
			replace_line('Current_Oponnent.txt', 0,  'Terran IIIIIIIII ' + str(new_Left_Num) )
		if(np.all((race_crop_left - left_zerg) == 0)):
			replace_line('Current_Oponnent.txt', 0,  'Zerg IIIIIIIII ' + str(new_Left_Num) )
		if(np.all((race_crop_left - left_protoss) == 0)):
			replace_line('Current_Oponnent.txt', 0,  'Protoss IIIIIIIII ' + str(new_Left_Num) )

	else:
		
		
		Eury_string = "Eurystheus"
		if(Eury_string in Right_Word):
			if(np.all((race_crop_left - left_terran) == 0)):
				replace_line('Current_Oponnent.txt', 0,  'Terran ' + new_Left_Word + " " + new_Left_Num )
			if(np.all((race_crop_left - left_zerg) == 0)):
				replace_line('Current_Oponnent.txt', 0,  'Zerg ' + new_Left_Word + " " + new_Left_Num )
			if(np.all((race_crop_left - left_protoss) == 0)):
				replace_line('Current_Oponnent.txt', 0,  'Protoss ' + new_Left_Word + " " + new_Left_Num )
		else:
			
			if(np.all((race_crop_right - right_terran) == 0)):
				replace_line('Current_Oponnent.txt', 0,  'Terran ' + new_Right_Word + " " + new_Right_Num )
			if(np.all((race_crop_right - right_zerg) == 0)):
				replace_line('Current_Oponnent.txt', 0,  'Zerg ' + new_Right_Word + " " + new_Right_Num )
			if(np.all((race_crop_right - right_protoss) == 0)):
				replace_line('Current_Oponnent.txt', 0,  'Protoss ' + new_Right_Word + " " + new_Right_Num )

	



