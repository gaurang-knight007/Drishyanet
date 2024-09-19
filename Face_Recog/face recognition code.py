import face_recognition
import cv2
import numpy as np
import os
import xlwt
from xlwt import Workbook
from datetime import date
import xlrd, xlwt
from xlutils.copy import copy as xl_copy
import time

CurrentFolder = os.getcwd() #Read current folder path
image1 = CurrentFolder+'\\gaurang.png'
image2 = CurrentFolder+'\\nandini.png'
image3 = CurrentFolder+'\\hansika.png'
image4 = CurrentFolder+'\\harsh_tiwari.png'
image5 = CurrentFolder+'\\hariom.png'
image6 = CurrentFolder+'\\gaurav.png'

video_capture = cv2.VideoCapture(0)

person1_name = "Gaurang"
person1_image = face_recognition.load_image_file(image1)
person1_face_encoding = face_recognition.face_encodings(person1_image)[0]

person2_name = "nandini"
person2_image = face_recognition.load_image_file(image2)
person2_face_encoding = face_recognition.face_encodings(person2_image)[0]

person3_name = "hansika"
person3_image = face_recognition.load_image_file(image3)
person3_face_encoding = face_recognition.face_encodings(person3_image)[0]

person4_name = "harsh tiwari"
person4_image = face_recognition.load_image_file(image4)
person4_face_encoding = face_recognition.face_encodings(person4_image)[0]

person5_name = "hariom"
person5_image = face_recognition.load_image_file(image5)
person5_face_encoding = face_recognition.face_encodings(person5_image)[0]

person6_name = "gaurav"
person6_image = face_recognition.load_image_file(image6)
person6_face_encoding = face_recognition.face_encodings(person6_image)[0]



# Create arrays of known face encodings and their names
known_face_encodings = [person1_face_encoding, person2_face_encoding, person3_face_encoding, person4_face_encoding, person5_face_encoding, person6_face_encoding]
known_face_names = [person1_name, person2_name, person3_name, person4_name, person5_name, person6_name]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

rb = xlrd.open_workbook('attendence_excel.xls', formatting_info=True)
wb = xl_copy(rb)
inp = input('Please give current subject lecture name')
sheet1 = wb.add_sheet(inp)
sheet1.write(0, 0, 'Name/Date')
sheet1.write(0, 1, str(date.today()))
row=1
col=0
already_attendence_taken = ""
last_marked_time = 0
marking_cooldown = 10 

while True:
    ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
            current_time = time.time()
            if ((already_attendence_taken != name) and (name != "Unknown") and (current_time - last_marked_time > marking_cooldown)):
                sheet1.write(row, col, name )
                col =col+1
                sheet1.write(row, col, "Present" )
                row = row+1
                col = 0
                print("attendence taken")
                wb.save('attendence_excel.xls')
                already_attendence_taken = name
                last_marked_time = current_time
            else:
                print("next student")
                break

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        print("data save")
        break

video_capture.release()
cv2.destroyAllWindows()

