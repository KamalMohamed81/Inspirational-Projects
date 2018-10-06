import os
import cv2
import numpy as np
import sqlite3


def insertOrUpdate(Id,Name,Age,Gen,Sector):
    conn=sqlite3.connect(os.path.join(os.path.dirname(__file__), "SQLdb/" + "WorkersInfo.db"))
    cursor = conn.execute("SELECT * FROM Workers WHERE ID = ?",(Id))
    data_exist=0
    for row in cursor:
        data_exist =1
    if(data_exist==1):
        conn.execute("UPDATE Workers SET Name = ? WHERE ID = ?",(Name, Id))
        conn.execute("UPDATE Workers SET Age = ? WHERE ID = ?",(Age, Id))
        conn.execute("UPDATE Workers SET Gender = ? WHERE ID = ?",(Gen, Id))
        conn.execute("UPDATE Workers SET Sector = ? WHERE ID = ?",(Sector, Id))
    else:
        cmd=conn.execute("INSERT INTO Workers(ID, Name, Age, Gender, Sector) VALUES(?,?,?,?,?)",(Id,Name,Age,Gen,Sector))
        cmd2=""
        cmd3=""
        cmd4=""
    conn.commit()
    conn.close()

Id_number=input('Enter Worker\'s Id : ')
name=input('Enter Worker\'s Name : ')
age=input('Enter Worker\'s Age : ')
gen=input('Enter Worker\'s Gender : ')
sector=input('Enter Worker\'s Sector : ')
insertOrUpdate(Id_number,name,age,gen,sector)
############################################################################################################################
worker_folder = "Worker" + str(Id_number) + "-" + name
sector_folder = "Sector" + " " + sector
directory_to_DATABASE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "DATABASE/"+ sector_folder + "/" + worker_folder)
print(directory_to_DATABASE)
if (os.path.exists(directory_to_DATABASE) == False):
    os.makedirs(directory_to_DATABASE)
############################################################################################################################
face_casc = cv2.CascadeClassifier('/home/KamalMohamed-Fedora/Programming/imageprocessing/trainedClassifiers/haarcascade_frontalface_default.xml')
eyes_casc = cv2.CascadeClassifier('/home/KamalMohamed-Fedora/Programming/imageprocessing/trainedClassifiers/haarcascade_eye.xml')
cam = cv2.VideoCapture(0)
samples_of_images_of_workers = 0
while True :
    ret, img = cam.read()
    if ret : 
        print("Incoming Camera Feed...")
    else :
        print("No Camera Feed ...")
    gray_sc = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_casc.detectMultiScale(gray_sc,1.3,5)
    for (x,y,z,h) in faces :
        samples_of_images_of_workers += 1
        cv2.imwrite(directory_to_DATABASE + "/Worker" + str(Id_number) + "-" + name + "." + str(samples_of_images_of_workers) + ".jpg", gray_sc[y:y+h,x:x+z])
        cv2.rectangle(img,(x,y),(x+z,y+h),(255,0,0),2)
        eyes_grays= gray_sc[y:y+h,x:x+z]
        eyes_normal= img[y:y+h,x:x+z]
        eyes = eyes_casc.detectMultiScale(eyes_grays,1.3,5)
        for (ex,ey,ez,eh) in eyes :
            cv2.rectangle(eyes_normal,(ex,ey),(ex+ez,ey+eh),(0,255,0),2)
        cv2.waitKey(100)
    cv2.imshow('Video',img)
    if ((cv2.waitKey(1) & 0xFF == ord('q')) | (samples_of_images_of_workers > 20 )) : 
        break
cam.release()
cv2.destroyAllWindows()
