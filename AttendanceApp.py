import face_recognition
import cv2
from PIL import Image, ImageDraw, ImageFont
import sys
import pandas as pd
import datetime
import pygame
import time


# module 1: refrence data load module

ef=pd.read_csv('DataFiles\\Employee.csv')
empno=ef["Employee No"].tolist()
name=ef["Name"].tolist()
photolocation=ef["Photo Location"].tolist()
audiolocation=ef["Audio Location"].tolist()

n=len(empno)
emp=[]
emp_encod=[]
audio=[]
for i in range(n):
    print(str(i)+" "+str(empno[i])+" "+name[i])
    emp.append(face_recognition.load_image_file(photolocation[i]))
    emp_encod.append(face_recognition.face_encodings(emp[i])[0])


#  module 2: face capture

camera=cv2.VideoCapture(0)
for i in range(10):
    return_value,image=camera.read()
    cv2.imwrite('Employee'+str(i)+'.png',image)

del(camera)


# module 3: face reconiton module 

uk=face_recognition.load_image_file('Employee5.png')
print(uk.shape)

def identify_employee(photo):
    try:
        uk_encode=face_recognition.face_encodings(photo)[0]
    except IndexError as e:
        print(e)
        sys.exit(1)
    found=face_recognition.compare_faces(emp_encod,
                                         uk_encode,tolerance=0.5)
    print(found)

    index=-1
    for i in range(n):
        if found[i]:
            index=i
    return (index)

emp_index=identify_employee(uk)
print(emp_index)

#  module 4: attendance record in a data file attendance.txt

if(emp_index!=-1):
    x=str(datetime.datetime.now())
    eno=str(empno[emp_index])
    nam=name[emp_index]
    ar="\n"+eno+" "+nam+" "+x
    f=open("DataFiles\\Attendance.txt","a")
    f.write(ar)
    f.close()
    print(ar)



# module 5: display attendance module

pil_uk=Image.fromarray(uk)
draw=ImageDraw.Draw(pil_uk)
fnt=ImageFont.truetype("C:\WINDOWS\FONTS\ITCBLKAD.TTF",30)

if emp_index==-1:
    name="Face Not Recognised"
else :
    name=name[emp_index]
x=100
y=uk.shape[0]-100
draw.text((x,y),name,font=fnt,fill=(250,0,0))
pil_uk.show()


# module 6: announce attendance recorded module

audioloc=audiolocation[emp_index]
pygame.mixer.init()

if(emp_index==-1):
    pygame.mixer.music.load("DataFiles\\EmployeeAudio\\retry.mp3")
    pygame.mixer.music.play()
    time.sleep(3) # Add a delay of 3 seconds
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up
    pygame.mixer.music.stop()
    pygame.mixer.quit()
else:
    pygame.mixer.music.load(audioloc)
    pygame.mixer.music.play()
    time.sleep(3) # Add a delay of 3 seconds
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    
print("Thank You!")